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

CROSSWALK = json.loads((ROOT / "probe" / "crosswalk.json").read_text())
PAIRS = {p["id"]: p for p in CROSSWALK["pairs"]}

# Grades where a comparison may be drawn on one axis. Everything else is a
# human judgment that it may not, and this server honours that judgment rather
# than second-guessing it -- the same veto the pair probe applies.
CHARTABLE = {"DIRECT", "PROXY"}

SKILL = """# NYC ↔ UN benchmark researcher

You are answering questions about how New York City compares to the UN's
authoritative global statistics.

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
- **NO-NYC-SOURCE / NO-SIGNAL** — no NYC counterpart, or the indicator is flat
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
    names = {x[0]: x[1] for x in ((r.get("entityMetadata") or {}).get("rows") or [])}
    rows = [x for x in ((r.get("data") or {}).get("rows") or []) if x[2] is not None]
    vals = [(x[2], names.get(x[0], x[0])) for x in rows]
    _keys = [x[0] for x in rows]
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
            "note": ("Lower rank = lower value. Tier 3 places a CITY against whole "
                     "NATIONS, which is context rather than a peer comparison."),
            "caveat": p["reason"]}


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
