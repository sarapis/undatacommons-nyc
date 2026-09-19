#!/usr/bin/env python3
"""NYC ↔ UN benchmark MCP server.

Composes the UN System Data Commons with NYC Open Data and serves the graded
crosswalk over MCP, so an agent can ask for a benchmark in one call.

THE POINT OF THIS SERVER IS THAT IT REFUSES.

Most tooling answers. This one returns a comparison only where a human has
graded the pair DIRECT or PROXY. For CONTEXT, BLOCKED and RANK-ONLY pairs it
declines and names the definitional difference that stopped it -- because the
failure mode we keep finding is not a missing number, it is a plausible chart
built on two things that were never the same measurement.

Stdio JSON-RPC, stdlib only: no framework, no virtualenv. Run it with

    python3 mcp/server.py

and point any MCP client at that command.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "probe"))

from undc import Client, UNDCError          # noqa: E402
import nyc                                   # noqa: E402
import census                                # noqa: E402
import country_names                         # noqa: E402

CROSSWALK = json.loads((ROOT / "probe" / "crosswalk.json").read_text())
PAIRS = {p["id"]: p for p in CROSSWALK["pairs"]}

ARTIFACTS = ROOT / "docs" / "artifacts"


def _latest(glob):
    """Newest artifact matching a glob, or None.

    Every one of these is committed, so a clean clone can answer without
    re-running a probe. A missing artifact returns None and the tool says so
    rather than pretending the answer is zero -- which is the failure this whole
    project keeps finding.
    """
    hits = sorted(ARTIFACTS.glob(glob))
    return json.loads(hits[-1].read_text()) if hits else None

# Grades where a comparison may be drawn on one axis. Everything else is a
# human judgment that it may not, and this server honours that judgment rather
# than second-guessing it -- the same veto the pair probe applies.
CHARTABLE = {"DIRECT", "PROXY"}

SKILL = """# NYC ↔ UN benchmark researcher

You are answering questions about how New York City compares to the UN's
authoritative global statistics.

Seven tools, and three of them answer questions the other four cannot:

- `reportable_gaps` — the United States reports NOTHING for 130 of the 442
  usable indicators. On those, NYC against the world is not a weaker comparison
  than NYC against the US; it is the only one available. Every row is ungraded.
- `framework_coverage` — does an indicator for this concept exist at all? None
  of the 519 named base indicators mentions an election, a vote or a turnout.
  A zero here is a finding about the framework, not about a city.
- `data_quality` — before quoting any UN figure, check whether a sweep of
  773,335 observations flagged it. Rows marked `verified_error` were confirmed
  by hand; everything else is an unreviewed question, not a defect.

## Before anything else

Call `list_benchmarks` to see which indicators are mapped and how each is
graded. Do not assume an indicator is available because it exists in the SDG
framework -- of 689 base indicators, 12 are mapped to NYC by hand and only a
handful can honestly share an axis.

## Read the grade before you read the number

- **PROXY / DIRECT** — may be charted together. Still carries a caveat; quote it.
- **CONTEXT** — the two numbers measure different things. Show them side by side
  if you must, never on one axis, and lead with the difference.
- **BLOCKED** — a comparison cannot be made at all. Say why.
- **RANK-ONLY** — NYC can be placed among countries for a single year and cannot
  be tracked against them over time.
- **NO-SOURCE / NO-SIGNAL** — no local counterpart, or the indicator is flat
  everywhere and carries no information.

`benchmark` refuses on anything outside PROXY/DIRECT. That refusal is the
answer, not an error: report the reason to the user rather than routing around
it or reaching for the raw numbers yourself.

## Always carry the provenance

Every value comes back with its source, vintage and unit. Never present a figure
without them. The UN side is often a *modelled estimate* where the NYC side is an
administrative count; that difference changes what a reader may conclude.

## Tiers say what a comparison is worth

- **Tier 1** — NYC against other countries' city aggregates. Like-for-like.
- **Tier 2** — against urban aggregates, which bundle cities with suburbs.
- **Tier 3** — against whole nations. Real context, not a peer comparison:
  cities generally run above their national averages.
"""


# --------------------------------------------------------------------------
# data access
# --------------------------------------------------------------------------

def _un_series(pair):
    c = Client(pause=0.3)
    o = c.get_observations(pair["un"]["dcid"], pair["un"]["place"], date="all")
    rows = (o.get("data") or {}).get("rows") or []
    src = o.get("sourceMetadata") or {}
    return ({str(r[1])[:4]: r[2] for r in rows},
            {"variable": (o.get("variable") or {}).get("name"),
             "dcid": pair["un"]["dcid"],
             "unit": (src.get("unit") or "").split("UNIT_MEASURE-")[-1],
             "provenance": src.get("provenanceUrl"),
             "observation_period": src.get("observationPeriod")})


def _nyc_series(pair):
    spec = pair.get("nyc")
    if not spec:
        return {}, {"note": "no NYC counterpart identified"}
    rows = nyc.query(spec["dataset"], spec["soql"])
    yf, vf = spec.get("year_field", "yr"), spec.get("value_field", "value")
    vals = {}
    for r in rows:
        y = str(r.get(yf, ""))[:4]
        if y.isdigit() and r.get(vf) is not None:
            vals[y] = float(r[vf])
    meta = {"dataset": spec["dataset"], "unit": spec.get("unit")}

    den = pair.get("denominator")
    if den and vals:
        years = [int(y) for y in vals]
        pop, _ = census.nyc_population(range(min(years), max(years) + 1))
        per = den.get("per", 100000)
        rated, dropped = {}, []
        for y, v in vals.items():
            if int(y) in pop:
                rated[y] = v / pop[int(y)] * per
            else:
                dropped.append(int(y))
        vals = rated
        meta["unit"] = den.get("unit", "per 100k")
        meta["denominator"] = den.get("source")
        # Years with no denominator are absent, never interpolated: an invented
        # rate is indistinguishable from a measured one.
        meta["years_without_denominator"] = sorted(dropped)
    return vals, meta


def _country_populations(client, year):
    """Country populations for a year, to turn national totals into per capita."""
    r = client.call_tool("get_child_observations",
                         {"variable_dcid": "undata/unicef/DM_POP",
                          "parent_place_dcid": "Earth", "child_place_type": "Country",
                          "date": str(year)})
    return {x[0]: x[2] for x in ((r.get("data") or {}).get("rows") or []) if x[2]}


def _find(name):
    """Resolve a loose name to a pair.

    Substring matching is not enough: "road deaths" is neither a substring of
    "Road traffic deaths" nor of the id "road-deaths". Match on word overlap
    instead, and take the best-scoring pair.
    """
    key = (name or "").strip().lower()
    if not key:
        return None
    if key in PAIRS:
        return PAIRS[key]
    words = set(re.findall(r"[a-z0-9]+", key))
    scored = []
    for p in PAIRS.values():
        hay = set(re.findall(r"[a-z0-9]+", f"{p['id']} {p['label']} {p['sdg']}".lower()))
        n = len(words & hay)
        if n:
            scored.append((n, p))
    if not scored:
        return None
    top = max(n for n, _ in scored)
    winners = [p for n, p in scored if n == top]
    if len(winners) > 1:
        # Two waste indicators tie on "municipal waste". Picking one silently is
        # exactly the kind of quiet guess this server exists not to make.
        return {"_ambiguous": [{"id": p["id"], "label": p["label"], "grade": p["grade"]}
                               for p in winners]}
    return winners[0]


# --------------------------------------------------------------------------
# tools
# --------------------------------------------------------------------------

def t_list_benchmarks(_args):
    return {"mapped": len(PAIRS),
            "note": "Grades are human judgments recorded in probe/crosswalk.json. "
                    "`benchmark` returns figures only for DIRECT and PROXY.",
            "benchmarks": [
                {"id": p["id"], "label": p["label"], "sdg": p["sdg"],
                 "tier": p.get("tier"), "grade": p["grade"],
                 "chartable": p["grade"] in CHARTABLE}
                for p in PAIRS.values()]}


def _resolve(args):
    """Return (pair, error). Exactly one of them is None."""
    p = _find(args.get("indicator"))
    if isinstance(p, dict) and "_ambiguous" in p:
        return None, {"error": f"{args.get('indicator')!r} matches more than one indicator",
                      "candidates": p["_ambiguous"],
                      "guidance": "Call again with an id from candidates."}
    if not p:
        return None, {"error": f"no mapped indicator matching {args.get('indicator')!r}",
                      "available": [x["id"] for x in PAIRS.values()]}
    return p, None


def t_explain_grade(args):
    p, err = _resolve(args)
    if err:
        return err
    if not p:
        return {"error": "unresolved"}
    return {"id": p["id"], "label": p["label"], "sdg": p["sdg"],
            "tier": p.get("tier"), "grade": p["grade"], "reason": p["reason"],
            "chartable": p["grade"] in CHARTABLE}


def t_benchmark(args):
    """Return a benchmark card -- or refuse, with the reason."""
    p, err = _resolve(args)
    if err:
        return err

    if p["grade"] not in CHARTABLE:
        return {"refused": True, "id": p["id"], "label": p["label"],
                "grade": p["grade"], "tier": p.get("tier"),
                "reason": p["reason"],
                "guidance": (
                    "This is a refusal, not an error. These two numbers must not "
                    "share an axis. Report the reason to the user; do not route "
                    "around it by fetching the sides separately."),
                "what_is_possible": {
                    "RANK-ONLY": "Ask world_position for a single-year ranking.",
                    "CONTEXT": "Show the two series side by side, clearly labelled "
                               "as different measures, never on one axis.",
                    "BLOCKED": "Nothing, until the blocker named above is resolved.",
                }.get(p["grade"], "Nothing until the grade changes.")}

    un, un_meta = _un_series(p)
    ny, ny_meta = _nyc_series(p)

    if not un:
        # Not an error. Some indicators have no comparator at all -- the US
        # reports municipal waste collected to nobody -- and that absence is
        # itself the finding.
        return {"refused": True, "id": p["id"], "label": p["label"],
                "grade": p["grade"], "tier": p.get("tier"),
                "reason": (f"The UN holds no observations of {p['un']['dcid']} for "
                           f"{p['un']['place']}. There is no comparator series to chart "
                           f"against."),
                "guidance": "Not a gap in this tool. The declared comparator reports nothing.",
                "what_is_possible": "Call world_position: other countries do report this, "
                                    "so NYC can still be placed among them."}

    overlap = sorted(set(un) & set(ny))
    year = str(args.get("year") or (overlap[-1] if overlap else ""))
    if year not in overlap:
        return {"error": f"no overlapping data for {year!r}",
                "overlap_years": overlap}

    return {"refused": False, "id": p["id"], "label": p["label"], "sdg": p["sdg"],
            "tier": p.get("tier"), "grade": p["grade"], "year": year,
            "nyc": {"value": round(ny[year], 3), **ny_meta},
            "comparator": {"value": round(un[year], 3), "place": p["un"]["place"],
                           **un_meta},
            "caveat": p["reason"],
            "overlap_years": [overlap[0], overlap[-1]]}


def t_world_position(args):
    """Place NYC among every reporting country for one year."""
    p, err = _resolve(args)
    if err:
        return err
    year = str(args.get("year") or "2019")

    c = Client(pause=0.3)
    try:
        r = c.call_tool("get_child_observations",
                        {"variable_dcid": p["un"]["dcid"], "parent_place_dcid": "Earth",
                         "child_place_type": "Country", "date": year})
    except UNDCError as exc:
        return {"error": str(exc)}
    # The platform names only ~155 of the places in a response and drops the alphabetical
    # tail without saying so (probe/country_names.py). Live names first, the measured cache
    # for the rest, and an ISO code -- never a bare DCID -- where neither has one.
    names = country_names.names_for(r)
    rows = [x for x in ((r.get("data") or {}).get("rows") or []) if x[2] is not None]
    vals = [(x[2], country_names.label(x[0], names)) for x in rows]
    _keys = [x[0] for x in rows]
    unnamed = sorted(x[0] for x in rows if x[0] not in names)
    if not vals:
        return {"error": f"no country data for {year}",
                "note": "Pick a year the indicator was actually collected in; "
                        "many are published in rounds, not annually."}

    ny, ny_meta = _nyc_series(p)
    if year not in ny:
        return {"error": f"no NYC value for {year}", "nyc_years": sorted(ny)[:40]}
    v = ny[year]

    der = p.get("derive")
    if der and der.get("per_capita"):
        # Both sides are absolute totals; compare them per person or not at all.
        pop, _ = census.nyc_population([int(year)])
        if int(year) not in pop:
            return {"error": f"no NYC population for {year}; cannot derive per capita"}
        v = v * der["nyc_multiplier"] / pop[int(year)]
        cpop = _country_populations(c, year)
        per = []
        for (x, n), k in zip(vals, _keys):
            if cpop.get(k):
                per.append((x * der["un_multiplier"] / cpop[k], n))
        vals = per
        ny_meta["unit"] = der["unit"]
        ny_meta["derivation"] = der["note"]

    vals.sort(key=lambda t: t[0])
    better = sum(1 for x, _ in vals if x < v)
    lo, hi = max(0, better - 2), min(len(vals), better + 2)
    return {"id": p["id"], "label": p["label"], "year": year, "tier": p.get("tier"),
            "nyc_value": round(v, 3), "unit": ny_meta.get("unit"),
            "rank": better + 1, "of": len(vals) + 1,
            "neighbours": [{"place": n, "value": round(x, 3)} for x, n in vals[lo:hi]],
            "unnamed_places": unnamed,
            "note": ("Lower rank = lower value. Tier 3 places a CITY against whole "
                     "NATIONS, which is context rather than a peer comparison."),
            "caveat": p["reason"]}



# The five findings a human checked against each indicator's own distribution
# and confirmed as errors, written up at
# docs/findings/2026-09-16-data-quality-report.md. Everything else the sweep
# raised is an unreviewed flag, and a tool that cannot tell a caller which is
# which is handing them the same ambiguity the sweep started with.
VERIFIED_ERRORS = {
    ("undata/sdg/VC_SNS_WALN_DRK", "Kyrgyzstan"):
        "x100 scale error 2021-23: 6710/6840/6990 where every other observation "
        "in the indicator falls between 22.8 and 95.0.",
    ("undata/sdg/EN_MWT_RCYV", "South Africa"):
        "Reads as kilograms: 1.86-3.44 billion tonnes recycled, against world "
        "municipal waste generation near 2 billion tonnes.",
    ("undata/sdg/EN_HAZ_PCAP", "Brunei"):
        "National total in a per-capita field: divide by Brunei's population and "
        "it lands on 28 kg against a global median of 22.",
    ("undata/sdg/EN_EWT_COLLPCAP", "Guadeloupe"):
        "x1,000 slip in the 2022 submission, propagated through all four e-waste "
        "indicators; makes a territory of 380,000 the world's largest recycler.",
    ("undata/sdg/SI_RMT_COST", "Malawi"):
        "Negative remittance cost, -0.10 and -0.93, between 13.13 and 31.48.",
}


def t_reportable_gaps(args):
    """Indicators the US does not report, which a city could."""
    art = _latest("us-silent-*.json")
    if not art:
        return {"error": "no us-silent artifact in docs/artifacts",
                "fix": "python3 probe/us_silent.py"}
    theme = (args.get("theme") or "").strip().lower()
    rows = art["indicators"]
    if theme:
        rows = [r for r in rows if theme in r["name"].lower()]
    min_peers = int(args.get("min_countries") or 0)
    rows = [r for r in rows if (r["world"] or {}).get("countries", 0) >= min_peers]
    rows.sort(key=lambda r: -((r["world"] or {}).get("countries") or 0))

    out = []
    for r in rows[:int(args.get("limit") or 25)]:
        w = r["world"] or {}
        c = (r["nyc_candidates"] or [None])[0]
        out.append({
            "dcid": r["dcid"], "indicator": r["name"],
            "reporting_countries": w.get("countries"),
            "years": (f"{w.get('first')}" if w.get("first") == w.get("last")
                      else f"{w.get('first')}-{w.get('last')}"),
            "single_year_level_only": w.get("first") == w.get("last"),
            "unit": w.get("unit"), "us_observations": w.get("us_obs"),
            "provenance": w.get("provenance"),
            "nyc_candidate": ({"dataset": c["id"], "name": c["name"], "score": c["score"]}
                              if c else None),
            "graded": False})
    return {
        "generated": art["generated"],
        "us_silent_usable": art["us_silent_usable"],
        "place_measurable": art["city_scoped"],
        "returned": len(out),
        "what_this_is": "Indicators the United States reports nothing for, so NYC against the "
                        "world is not a weaker comparison than NYC against the US -- it is the "
                        "only one available. US absence was verified against the country "
                        "observations, not inherited from the screening proxy.",
        "not_a_crosswalk": "Every row is graded:false. The NYC candidate is a proposal from an "
                           "embedding matcher whose precision on hand-read lists is roughly half. "
                           "Under comparability spec v0.1 a grade is a human judgment, so none of "
                           "these is a mapping until a person makes it one.",
        "indicators": out}


def t_framework_coverage(args):
    """Does the SDG framework have an indicator for a concept at all?

    The inverse of everything else here. `benchmark` asks what the UN holds for
    an indicator; this asks whether the framework has an indicator at all -- the
    question that found that none of the 519 named base indicators mentions an
    election, a vote or a turnout.
    """
    concept = (args.get("concept") or "").strip()
    if not concept:
        return {"error": "concept is required",
                "example": {"concept": "election voting turnout"}}
    screened = json.loads((ROOT / "probe" / "cache" / "screened.json").read_text())
    named = [(r["dcid"], r["name"]) for r in screened["indicators"] if r.get("name")]
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z-]{2,}", concept.lower())]
    if not words:
        return {"error": f"no searchable words in {concept!r}"}
    pat = re.compile("|".join(re.escape(w) for w in words), re.I)
    hits = [{"dcid": d, "name": n} for d, n in named if pat.search(n)]

    out = {"concept": concept, "searched_terms": words,
           "named_indicators_searched": len(named),
           "matching_indicators": len(hits), "indicators": hits[:20],
           "caveat": "Lexical search over indicator NAMES. A concept the framework covers under "
                     "different words will not appear here, so a zero is a prompt to check the "
                     "wording, not proof of absence."}

    # Two categories have a measured municipal side; the rest do not, and the
    # tool says which it is rather than implying the count is missing.
    gaps = _latest("category-gaps-*.json") or {}
    for key, c in (gaps.get("categories") or {}).items():
        if any(w in key or w in c["label"].lower() for w in words):
            dom = c.get("top_city") or [None, 0]
            out["municipal_side"] = {
                "category": c["label"],
                "datasets": c["n_datasets"], "cities": c["n_cities"],
                "in_bottom_quartile": c["in_tail"],
                "most_concentrated_city": dom[0], "its_share_of_datasets": dom[1],
                "nearest_indicators_offered": [n for n, _ in c["nearest_offered"][:3]],
                "method": "Titles carrying the category's vocabulary in six languages -- "
                          "counted, not clustered. Cities are the unit of evidence, not "
                          "datasets: one city publishing three hundred files is a filing habit."}
            break
    else:
        out["municipal_side"] = {
            "measured": False,
            "note": "No precomputed municipal count for this concept. "
                    "Add it to CATEGORIES in probe/category_gaps.py and re-run."}
    return out


def t_data_quality(args):
    """Plausibility flags the corpus sweep raised against a UN series."""
    art = _latest("smell-*.json")
    if not art:
        return {"error": "no smell artifact in docs/artifacts",
                "fix": "python3 probe/smell.py --all"}
    q = (args.get("dcid") or args.get("indicator") or "").strip().lower()
    findings = art["findings"]
    if q:
        findings = [f for f in findings
                    if q in f["dcid"].lower() or q in (f.get("indicator") or "").lower()]
    sev = (args.get("severity") or "").strip().upper()
    if sev:
        findings = [f for f in findings if f["severity"] == sev]
    # Verified errors first, then by severity. A caller asking whether a series
    # is trustworthy wants the confirmed defect before the unreviewed flag.
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    def _verified(f):
        return VERIFIED_ERRORS.get((f["dcid"], f.get("place_name")))
    findings.sort(key=lambda f: (0 if _verified(f) else 1, order.get(f["severity"], 9)))
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    return {
        "generated": art["generated"], "scope": art["scope"],
        "observations_swept": art["observations"],
        "query": q or "(everything)", "matching_findings": len(findings),
        "by_severity": counts,
        # A verified error spans every year of its series -- Brunei's is eight
        # rows of one defect -- so report the series count, not the row count.
        "verified_error_rows": sum(1 for f in findings if _verified(f)),
        "verified_error_series": len({(f["dcid"], f.get("place_name"))
                                      for f in findings if _verified(f)}),
        "findings": [dict({k: f[k] for k in ("check", "severity", "dcid", "indicator",
                                             "place_name", "year", "value", "unit", "detail")
                           if k in f},
                          verified_error=_verified(f) or False)
                     for f in findings[:int(args.get("limit") or 20)]],
        "this_flags_it_does_not_judge":
            "A flag is a question for someone who knows the indicator, not a defect report. "
            "Kuwait's water stress above 100% is correct; so is a disaster-affected rate above "
            "its own population, because a person counts once per disaster. Rows carrying "
            "`verified_error` were checked by hand against the indicator's own distribution and "
            "confirmed; every other row is UNREVIEWED and should be treated as a question.",
    }


TOOLS = [
    {"name": "list_benchmarks",
     "description": "List every NYC↔UN indicator pair with its comparability grade and tier. "
                    "Call this first; most SDG indicators are not mapped, and several that are "
                    "cannot be charted.",
     "inputSchema": {"type": "object", "properties": {}},
     "handler": t_list_benchmarks},
    {"name": "benchmark",
     "description": "Compare NYC with its UN comparator for one indicator and year. REFUSES "
                    "unless a human graded the pair DIRECT or PROXY, returning the definitional "
                    "reason instead. Treat a refusal as the answer.",
     "inputSchema": {"type": "object",
                     "properties": {"indicator": {"type": "string"},
                                    "year": {"type": "string"}},
                     "required": ["indicator"]},
     "handler": t_benchmark},
    {"name": "world_position",
     "description": "Place NYC among every country reporting an indicator in a given year, with "
                    "its rank and nearest neighbours.",
     "inputSchema": {"type": "object",
                     "properties": {"indicator": {"type": "string"},
                                    "year": {"type": "string"}},
                     "required": ["indicator"]},
     "handler": t_world_position},
    {"name": "explain_grade",
     "description": "Why an indicator pair carries the grade it does -- the definitional "
                    "difference, the denominator problem, or the coverage gap behind it.",
     "inputSchema": {"type": "object",
                     "properties": {"indicator": {"type": "string"}},
                     "required": ["indicator"]},
     "handler": t_explain_grade},
    {"name": "reportable_gaps",
     "description": "Indicators the United States reports NOTHING for, which a city could report "
                    "-- where NYC against the world is the only comparison available. Returns "
                    "the peer group of reporting countries and an UNGRADED NYC candidate.",
     "inputSchema": {"type": "object",
                     "properties": {"theme": {"type": "string",
                                              "description": "substring filter, e.g. 'waste'"},
                                    "min_countries": {"type": "integer"},
                                    "limit": {"type": "integer"}}},
     "handler": t_reportable_gaps},
    {"name": "framework_coverage",
     "description": "Does the SDG framework have an indicator for a concept at all? Searches "
                    "every named base indicator. This is how we found that none of the 519 "
                    "mentions an election, a vote or a turnout.",
     "inputSchema": {"type": "object",
                     "properties": {"concept": {"type": "string"}},
                     "required": ["concept"]},
     "handler": t_framework_coverage},
    {"name": "data_quality",
     "description": "Plausibility flags raised against a UN series by a sweep of 773,335 "
                    "observations -- impossible percentages, scale errors, values far outside "
                    "an indicator's own distribution. Check before quoting a figure.",
     "inputSchema": {"type": "object",
                     "properties": {"dcid": {"type": "string"},
                                    "severity": {"type": "string",
                                                 "enum": ["HIGH", "MEDIUM", "LOW"]},
                                    "limit": {"type": "integer"}}},
     "handler": t_data_quality},
]
HANDLERS = {t["name"]: t.pop("handler") for t in TOOLS}

RESOURCES = [{"uri": "skill://nyc-benchmark-researcher/SKILL.md",
              "name": "nyc-benchmark-researcher/SKILL.md",
              "description": "How to read grades, tiers and refusals before quoting any figure.",
              "mimeType": "text/markdown"}]


# --------------------------------------------------------------------------
# JSON-RPC over stdio
# --------------------------------------------------------------------------

def handle(msg):
    method, mid = msg.get("method"), msg.get("id")
    if method == "initialize":
        return {"protocolVersion": "2025-06-18",
                "capabilities": {"tools": {}, "resources": {}},
                "serverInfo": {"name": "nyc-un-benchmarks", "version": "0.1.0"},
                "instructions": (
                    "Serves a hand-graded crosswalk between NYC Open Data and the UN System "
                    "Data Commons. Read skill://nyc-benchmark-researcher/SKILL.md before "
                    "calling any tool. `benchmark` refuses on pairs a human graded "
                    "incomparable; that refusal is the answer.")}
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "resources/list":
        return {"resources": RESOURCES}
    if method == "resources/read":
        return {"contents": [{"uri": msg["params"]["uri"], "mimeType": "text/markdown",
                              "text": SKILL}]}
    if method == "tools/call":
        name = msg["params"]["name"]
        fn = HANDLERS.get(name)
        if not fn:
            raise ValueError(f"unknown tool {name}")
        out = fn(msg["params"].get("arguments") or {})
        return {"content": [{"type": "text", "text": json.dumps(out, indent=1)}],
                "structuredContent": out}
    if mid is None:
        return None                      # a notification; nothing to answer
    raise ValueError(f"unknown method {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        mid = msg.get("id")
        try:
            result = handle(msg)
        except Exception as exc:                        # noqa: BLE001
            if mid is not None:
                print(json.dumps({"jsonrpc": "2.0", "id": mid,
                                  "error": {"code": -32603, "message": str(exc)}}),
                      flush=True)
            continue
        if mid is not None and result is not None:
            print(json.dumps({"jsonrpc": "2.0", "id": mid, "result": result}), flush=True)


if __name__ == "__main__":
    main()
