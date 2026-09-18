#!/usr/bin/env python3
"""Smell test: plausibility checks on the UN graph, run from outside it.

Malaysia reports 147.7% of its municipal waste recycled. That is in authoritative
UN data, it is on our demo, and we found it by accident while building a chart.
This asks the obvious follow-up systematically: what else is in there?

The checks are cheap and dumb on purpose -- a percentage above 100, a negative
count, a rate exceeding its own denominator, a value repeated identically across
countries that should not agree. None of them require knowing the subject matter,
which is exactly why an outsider can run them.

**This flags; it does not judge.** A gross enrolment ratio above 100% is correct
(pupils outside the nominal age band are counted in the numerator and not the
denominator). A flatline can be a country that genuinely did not change. Every
finding here is a question for someone who knows the indicator, and the report
prints the indicator name next to every row so that person can answer it. Calling
these "errors" would be the same mistake as calling a matcher's shortlist a
crosswalk.

One `get_child_observations` call per indicator returns every country and every
year, so a sweep of the whole usable corpus is a few hundred calls rather than a
few hundred thousand.

Usage:
  python3 probe/smell.py                  # the 442 usable indicators
  python3 probe/smell.py --all            # every enumerated base indicator
  python3 probe/smell.py --resume         # continue an interrupted sweep
  python3 probe/smell.py --limit 20
Writes docs/artifacts/smell-<date>.{json,md}; progress in probe/cache/smell.json.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from undc import Client, UNDCError  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "probe" / "cache"
ARTIFACTS = ROOT / "docs" / "artifacts"
STATE = CACHE / "smell.json"
# Raw observations, so iterating on the checks costs nothing. Gitignored: this
# is ~770,000 rows. Three full re-sweeps were spent re-downloading it before
# this existed.
RAW = CACHE / "smell-raw.json"
SCREENED = CACHE / "screened.json"
CORPUS = CACHE / "corpus.json"

USABLE = ("GREEN", "AMBER", "RANK-ONLY")
THIS_YEAR = dt.date.today().year

# Unit DCIDs that mean "this is a percentage". A value outside 0-100 in one of
# these is at least worth a question.
PERCENT_UNITS = {"Percent", "PERCENT", "RATIO_COUNT_PERCENT", "PT", "PERCENTAGE"}

# A rate per N of some population cannot exceed N without more events than
# there are people to have them. Parsed rather than enumerated: the corpus uses
# PER_100, PER_1000, PER_100000 and PER_1000000 against POP, LIVEBIRTHS and
# POP_UNINFECTED, and a hardcoded list quietly sent four of those to the wrong
# branch -- RATIO_COUNT_PER_100_COUNT_POP was classified as a plain count
# because the string contains "COUNT", so its cap was never applied.
SCALED_RE = re.compile(r"^RATIO_COUNT_PER_(\d+)_COUNT_")

# Units that count things. A negative one is not a measurement. Checked only
# after SCALED_RE, which is the more specific pattern.
COUNT_HINTS = ("COUNT", "NUMBER", "DEATHS", "PERSON")

# How many consecutive identical values before a series looks carried forward
# rather than measured.
FLATLINE_RUN = 6
FLATLINE_ZERO_RUN = 10

# A year-on-year multiple this large is either a real shock, a revision, or a
# units change. All three are worth seeing.
JUMP_FACTOR = 10.0

# ...but only if the move is also big against the series' own scale. Without
# this, a series that idles near zero throws a "x50" every time it twitches.
JUMP_MIN_FRACTION_OF_SCALE = 0.05

# How many countries must share an identical high-precision value before it
# looks like a modelled default rather than a coincidence.
SHARED_VALUE_COUNTRIES = 5

# ...and how many decimal places make that agreement surprising. At two, a
# bounded index with 200 reporters produces collisions by pigeonhole alone.
SHARED_VALUE_DECIMALS = 3

# An indicator is its own control group.
#
# "Annual growth rate of real GDP per capita" is published with the unit
# `Percent` and is negative for 1,256 country-years, because a growth rate is
# signed by construction. So is "Current account balance as a proportion of
# GDP", and "Change in minimum river flow (%)". The first full sweep returned
# 23,172 negative percentages and every one I checked was correct -- the graph's
# `Percent` unit covers both bounded proportions and signed rates, and no unit
# string tells them apart.
#
# What does tell them apart is frequency. A rule violated by most of an
# indicator's observations is not a violation, it is the definition. A rule
# violated by three country-years out of three thousand is Malaysia recycling
# 147.7% of its municipal waste. So a check is suppressed for an indicator when
# it fires often enough to be structural -- and the suppression is REPORTED,
# because "these 34 indicators express signed percentages" is itself a finding
# about the graph's unit vocabulary.
RARITY_OBS_SHARE = 0.01        # observation-level checks
RARITY_SERIES_SHARE = 0.25     # series-level checks (flatlines)
RARITY_MIN_FINDINGS = 3        # one anomaly is never evidence of a definition

# A value this many times the indicator's own 99th percentile is not a big
# number, it is a different quantity. This is the check that survives
# suppression: "proportion of hazardous waste treated" exceeds 100% for 37
# countries, so its range check is structural and gets dropped -- but Guatemala
# at 44,825% is still 448x anything the indicator otherwise contains. Absolute
# bounds describe what a unit means; this describes what an indicator actually
# holds, and it is the only check that reaches the 123 indicators whose units
# (CR_USD, WEIGHT_TN, INDEX, SCORE) have no meaningful range at all.
OUTLIER_FACTOR = 20.0
OUTLIER_MIN_OBS = 50

SERIES_LEVEL_CHECKS = {"flatline", "flatline_zero"}
UNGATED_CHECKS = {"shared_value", "outlier"}  # rare by construction already

SEVERITY = {
    "outlier": "HIGH",
    "percent_negative": "HIGH",
    "negative_count": "HIGH",
    "rate_over_scale": "HIGH",
    "future_year": "HIGH",
    "percent_over_100": "MEDIUM",
    "jump": "MEDIUM",
    "shared_value": "MEDIUM",
    "flatline": "LOW",
    "flatline_zero": "LOW",
}

WHY = {
    "outlier": f"At least {OUTLIER_FACTOR:g}x the indicator's own 99th percentile across "
               "every country and year. Scale-free, so it survives when an absolute range "
               "check has been suppressed as structural — and it is the only check that "
               "reaches units with no meaningful range.",
    "percent_negative": "A percentage below zero is not a measurement.",
    "negative_count": "A count of things cannot be negative.",
    "rate_over_scale": "The rate exceeds its own denominator. Written expecting "
                       "'more events than there are people to have them' — but all four "
                       "hits are disaster-affected persons per 100,000, where a person "
                       "counts once per disaster, so exceeding the population is correct "
                       "for a country hit repeatedly in one year. The check stands because "
                       "the same shape on a rate that cannot repeat would be a real error; "
                       "the premise, as written, was wrong.",
    "future_year": f"Observation dated after {THIS_YEAR}.",
    "percent_over_100": "Above 100%. Sometimes correct — gross enrolment ratios count "
                        "pupils outside the nominal age band in the numerator only, and "
                        "Kuwait's water stress genuinely exceeds its renewable resources "
                        "— and sometimes it is Malaysia recycling 147.7% of its municipal "
                        "waste. Needs a human.",
    "jump": f"Changed by a factor of {JUMP_FACTOR:g}+ in one year, by a margin worth "
            f"{JUMP_MIN_FRACTION_OF_SCALE:.0%}+ of the series' own range. A real shock, a "
            "revision, or a units change. Only run on non-negative counts, rates and "
            "percentages — a ratio means nothing on a signed index.",
    "shared_value": f"An identical value carrying {SHARED_VALUE_DECIMALS}+ decimals, in "
                    f"{SHARED_VALUE_COUNTRIES}+ countries for the same year. Countries do "
                    "not agree to that precision by chance; this is the shape of a "
                    "modelled default.",
    "flatline": f"{FLATLINE_RUN}+ consecutive identical non-zero values. Either nothing "
                "changed, or a figure is being carried forward.",
    "flatline_zero": f"{FLATLINE_ZERO_RUN}+ consecutive zeros. Often true of small "
                     "states; occasionally a missing value written as 0.",
}


def unit_kind(unit):
    u = (unit or "").strip()
    if u in PERCENT_UNITS:
        return "percent"
    if SCALED_RE.match(u):
        return "scaled"
    if any(h in u.upper() for h in COUNT_HINTS):
        return "count"
    return "other"


def surprising_precision(v, places=SHARED_VALUE_DECIMALS):
    """Is agreeing on this number a coincidence worth remarking on?

    The first version accepted anything with two decimals, and promptly
    "discovered" that five of 201 countries shared a food-price index value of
    -0.11. On a scale spanning -2 to +3 at two decimals there are only a few
    hundred possible values and 201 countries, so collisions are what the
    pigeonhole principle predicts, not evidence of anything. Three or more
    decimals is where independent agreement stops being cheap.
    """
    scaled = v * (10 ** places)
    return abs(scaled - round(scaled)) > 1e-9 or _decimals(v) >= places


def _decimals(v):
    txt = f"{v!r}"
    return len(txt.split(".")[1]) if "." in txt and "e" not in txt.lower() else 0


def check_series(dcid, name, place, place_name, unit, kind, series, signed):
    """All checks for one country's series. series is [(year:int, value:float)]."""
    out = []

    def add(check, year, value, detail=""):
        out.append({"check": check, "severity": SEVERITY[check], "dcid": dcid,
                    "indicator": name, "place": place, "place_name": place_name,
                    "year": year, "value": value, "unit": unit, "detail": detail})

    for year, v in series:
        if year > THIS_YEAR:
            add("future_year", year, v)
        if kind == "percent":
            if v < 0:
                add("percent_negative", year, v)
            elif v > 100:
                add("percent_over_100", year, v)
        elif kind == "scaled":
            cap = int(SCALED_RE.match(unit).group(1))
            if v < 0:
                add("negative_count", year, v)
            elif v > cap:
                add("rate_over_scale", year, v, f"cap {cap:,}")
        elif kind == "count" and v < 0:
            add("negative_count", year, v)

    # Runs of identical values.
    run_start, run_val, run_len = None, None, 0
    def flush(end_year):
        if run_val is None:
            return
        threshold = FLATLINE_ZERO_RUN if run_val == 0 else FLATLINE_RUN
        if run_len >= threshold:
            add("flatline_zero" if run_val == 0 else "flatline", run_start, run_val,
                f"{run_len} consecutive years {run_start}–{end_year}")
    prev_year = None
    for year, v in series:
        contiguous = prev_year is not None and year == prev_year + 1
        if run_val is not None and v == run_val and contiguous:
            run_len += 1
        else:
            flush(prev_year)
            run_start, run_val, run_len = year, v, 1
        prev_year = year
    flush(prev_year)

    # Year-on-year jumps.
    #
    # A ratio only means something on a quantity with a real zero and positive
    # support. The Indicator of Food Price Anomalies is a SIGNED index centred
    # on zero: it crosses zero every few years, so 0.01 -> -0.54 scores "x54"
    # and is an ordinary move on that scale. Ungated, this check flagged 351 of
    # that one indicator's 3,005 observations -- 12%, which measures the check
    # rather than the data.
    #
    # Gate on the shape of the quantity, NOT on a list of units. The first
    # version whitelisted percent/count/rate units and thereby threw away
    # Mauritius' food waste going 207 tonnes -> 177,570 tonnes in one year --
    # an 859x move, precisely what this exists to find -- because `WEIGHT_TN`
    # was not on the list. `signed` is judged across the whole indicator: if any
    # country ever reports a negative, the quantity has no meaningful zero and
    # no ratio on it means anything.
    if not signed and all(v >= 0 for _, v in series):
        scale = max((abs(v) for _, v in series), default=0.0)
        for (y1, v1), (y2, v2) in zip(series, series[1:]):
            if y2 != y1 + 1 or v1 <= 0 or v2 <= 0:
                continue
            if abs(v2 - v1) < JUMP_MIN_FRACTION_OF_SCALE * scale:
                continue
            ratio = v2 / v1
            if ratio >= JUMP_FACTOR or ratio <= 1 / JUMP_FACTOR:
                add("jump", y2, v2, f"{v1:g} ({y1}) -> {v2:g} ({y2}), x{ratio:.1f}")
    return out


def check_outliers(dcid, name, unit, by_place):
    """Values extreme against the indicator's own distribution, not against a unit."""
    allv = [abs(v) for _, ser in by_place.values() for _, v in ser]
    if len(allv) < OUTLIER_MIN_OBS:
        return []
    allv.sort()
    p99 = allv[min(int(len(allv) * 0.99), len(allv) - 1)]
    if p99 <= 0:
        return []
    out = []
    for place, (pname, series) in by_place.items():
        for year, v in series:
            if abs(v) > OUTLIER_FACTOR * p99:
                out.append({"check": "outlier", "severity": SEVERITY["outlier"],
                            "dcid": dcid, "indicator": name, "place": place,
                            "place_name": pname or place, "year": year, "value": v,
                            "unit": unit,
                            "detail": f"{abs(v) / p99:,.0f}x the indicator's p99 "
                                      f"({p99:,.4g}); median {allv[len(allv) // 2]:,.4g}"})
    return out


def check_shared_values(dcid, name, unit, by_place):
    """One non-round value appearing in many countries for the same year."""
    out = []
    byyear = {}
    for place, (pname, series) in by_place.items():
        for year, v in series:
            if v == 0 or _decimals(v) < SHARED_VALUE_DECIMALS:
                continue
            byyear.setdefault((year, v), []).append(pname or place)
    for (year, v), places in sorted(byyear.items()):
        if len(places) >= SHARED_VALUE_COUNTRIES:
            out.append({"check": "shared_value", "severity": SEVERITY["shared_value"],
                        "dcid": dcid, "indicator": name, "place": "(multiple)",
                        "place_name": f"{len(places)} countries", "year": year,
                        "value": v, "unit": unit,
                        "detail": ", ".join(sorted(places)[:8])
                                  + (f" +{len(places) - 8} more" if len(places) > 8 else "")})
    return out


def sweep_one(client, dcid, raw=None):
    """Every country, every year, for one indicator. One call."""
    if raw is not None and dcid in raw:
        r = raw[dcid]
    else:
        r = client.call_tool("get_child_observations",
                             {"variable_dcid": dcid, "parent_place_dcid": "Earth",
                              "child_place_type": "Country", "date": "all"})
        if raw is not None:
            raw[dcid] = r
    name = (r.get("variable") or {}).get("name") or dcid
    src = r.get("sourceMetadata") or {}
    unit = (src.get("unit") or "").split("UNIT_MEASURE-")[-1]
    kind = unit_kind(unit)
    names = {x[0]: x[1] for x in ((r.get("entityMetadata") or {}).get("rows") or [])}

    by_place = {}
    n_obs = 0
    for row in ((r.get("data") or {}).get("rows") or []):
        place, date, value = row[0], str(row[1]), row[2]
        if value is None or not date[:4].isdigit():
            continue
        try:
            v = float(value)
        except (TypeError, ValueError):
            continue
        by_place.setdefault(place, [names.get(place), []])[1].append((int(date[:4]), v))
        n_obs += 1
    for place in by_place:
        by_place[place][1].sort()

    # An indicator-level property: does this quantity ever go negative anywhere?
    signed = any(v < 0 for _, ser in by_place.values() for _, v in ser) \
        or "INDEX" in (unit or "").upper()

    findings = []
    for place, (pname, series) in by_place.items():
        findings += check_series(dcid, name, place, pname, unit, kind, series, signed)
    flat = {p: (v[0], v[1]) for p, v in by_place.items()}
    findings += check_shared_values(dcid, name, unit, flat)
    findings += check_outliers(dcid, name, unit, flat)

    findings, suppressed = apply_rarity_gate(findings, n_obs, len(by_place))

    return {"dcid": dcid, "indicator": name, "unit": unit, "unit_kind": kind,
            "n_obs": n_obs, "n_places": len(by_place), "signed": signed,
            "provenance": src.get("provenanceUrl"),
            "findings": findings, "suppressed": suppressed}


def apply_rarity_gate(findings, n_obs, n_places):
    """Drop checks that fire so often for one indicator that they describe it.

    Returns (kept, suppressed). Suppressed groups are carried forward rather
    than discarded: the list of indicators whose percentages are routinely
    negative is a description of the graph's unit vocabulary, and hiding it
    would make this sweep look cleaner than the data is.
    """
    groups = {}
    for f in findings:
        groups.setdefault(f["check"], []).append(f)

    kept, suppressed = [], []
    for check, fs in groups.items():
        if check in UNGATED_CHECKS or len(fs) < RARITY_MIN_FINDINGS:
            kept += fs
            continue
        series_level = check in SERIES_LEVEL_CHECKS
        denom = max(n_places if series_level else n_obs, 1)
        share = len(fs) / denom
        limit = RARITY_SERIES_SHARE if series_level else RARITY_OBS_SHARE
        if share > limit:
            suppressed.append({
                "check": check, "dcid": fs[0]["dcid"], "indicator": fs[0]["indicator"],
                "unit": fs[0]["unit"], "n_findings": len(fs),
                "of": denom, "basis": "series" if series_level else "observations",
                "share": round(share, 4)})
        else:
            kept += fs
    return kept, suppressed


def load_targets(use_all, limit, corpus_path=None):
    if use_all:
        src = pathlib.Path(corpus_path) if corpus_path else CORPUS
        rows = [{"dcid": d, "name": None}
                for d in sorted(json.loads(src.read_text())["bases"])]
    else:
        rows = [{"dcid": r["dcid"], "name": r.get("name")}
                for r in json.loads(SCREENED.read_text())["indicators"]
                if r.get("grade") in USABLE]
        rows.sort(key=lambda r: r["dcid"])
    return rows[:limit] if limit else rows


def render(results, scope_label):
    today = dt.date.today().isoformat()
    findings = [f for r in results for f in r["findings"]]
    checked = [r for r in results if not r.get("error")]
    errored = [r for r in results if r.get("error")]
    n_obs = sum(r.get("n_obs", 0) for r in checked)

    by_check = {}
    for f in findings:
        by_check.setdefault(f["check"], []).append(f)
    order = sorted(by_check, key=lambda c: (["HIGH", "MEDIUM", "LOW"].index(SEVERITY[c]),
                                            -len(by_check[c])))

    md = ["---", "layout: default", f"title: UN graph smell test — {today}", "---", "",
          f"# UN graph smell test — {today}", "",
          "Plausibility checks run against the UN System Data Commons from outside it. "
          "The checks are deliberately dumb — a percentage above 100, a negative count, a "
          "rate exceeding its own denominator, one value repeated across countries that "
          "should not agree. None of them require subject-matter knowledge, which is why "
          "an outsider can run them at all.", "",
          "**This flags; it does not judge.** A gross enrolment ratio above 100% is "
          "*correct*. A flatline can be a country that genuinely did not change. Every row "
          "below is a question for someone who knows the indicator, not a defect report. "
          "The indicator name is printed against every row so that person can answer it.", "",
          f"**Scope:** {scope_label} — **{len(checked):,} indicators**, "
          f"**{n_obs:,} observations** across every reporting country and year."
          + (f" {len(errored)} indicator(s) did not return data." if errored else ""), "",
          f"**{len(findings):,} findings** across {len(by_check)} checks.", "",
          "### What the checks reach", "",
          "Range checks depend on knowing what the unit means. Most of the corpus is "
          "percentages and counts; the rest gets only the unit-agnostic checks (jump, "
          "flatline, shared value, future date). This table is here so the headline count "
          "is read against what was actually inspected.", "",
          "| Unit kind | Indicators | Observations | Range checks |", "|---|---:|---:|---|"]
    kinds = {}
    for r in checked:
        k = kinds.setdefault(r["unit_kind"], [0, 0])
        k[0] += 1
        k[1] += r.get("n_obs", 0)
    applies = {"percent": "yes — 0–100", "scaled": "yes — capped by denominator",
               "count": "yes — non-negative", "other": "**no** — unit-agnostic checks only"}
    for k in sorted(kinds, key=lambda k: -kinds[k][1]):
        md.append(f"| {k} | {kinds[k][0]} | {kinds[k][1]:,} | {applies[k]} |")
    md += ["",
          "| Check | Severity | Findings | Indicators | What it means |",
          "|---|---|---:|---:|---|"]
    for c in order:
        fs = by_check[c]
        md.append(f"| `{c}` | {SEVERITY[c]} | {len(fs):,} | "
                  f"{len({f['dcid'] for f in fs}):,} | {WHY[c]} |")

    for c in order:
        fs = by_check[c]
        sev = SEVERITY[c]
        # Every HIGH row is printed. The noisier low-severity checks are capped,
        # and the cap is stated rather than quietly applied.
        cap = None if sev == "HIGH" else 60
        shown = fs if cap is None else fs[:cap]
        md += ["", f"## `{c}` — {sev} · {len(fs):,} findings", "", WHY[c], ""]
        if cap is not None and len(fs) > cap:
            md.append(f"*Showing the first {cap} of {len(fs):,}. "
                      f"The full set is in the JSON beside this page.*\n")
        md += ["| Indicator | Place | Year | Value | Unit | Detail |", "|---|---|---:|---:|---|---|"]
        for f in shown:
            ind = f["indicator"][:64]
            det = (f.get("detail") or "")[:70]
            md.append(f"| {ind} | {f['place_name'] or f['place']} | {f['year']} | "
                      f"{f['value']:g} | `{f['unit']}` | {det} |")

    suppressed = [x for r in results for x in r.get("suppressed", [])]
    if suppressed:
        by_s = {}
        for x in suppressed:
            by_s.setdefault(x["check"], []).append(x)
        md += ["", "## Suppressed as structural", "",
               "A rule violated by most of an indicator's observations is not a violation, "
               "it is the definition. These (indicator, check) pairs fired often enough to "
               "be structural and were dropped from the findings above — listed here "
               "because the list is itself a result.", "",
               f"**{len(suppressed)} suppressed groups** covering "
               f"{sum(x['n_findings'] for x in suppressed):,} would-be findings.", ""]
        for c in sorted(by_s, key=lambda c: -len(by_s[c])):
            xs = sorted(by_s[c], key=lambda x: -x["n_findings"])
            md += [f"### `{c}` — {len(xs)} indicators", "",
                   "| Indicator | Unit | Fired | Of | Share |", "|---|---|---:|---:|---:|"]
            for x in xs:
                md.append(f"| {x['indicator'][:72]} | `{x['unit']}` | {x['n_findings']:,} | "
                          f"{x['of']:,} {x['basis']} | {x['share']:.0%} |")
            md.append("")

    if errored:
        md += ["", "## Indicators that returned nothing", "",
               "Not findings — the sweep asks every usable indicator for world data and "
               "some have none at country level.", ""]
        for r in errored[:40]:
            md.append(f"- `{r['dcid']}` — {r['error'][:110]}")

    md += ["", "## Reproducing", "", "```bash", "python3 probe/smell.py", "```", "",
           "One `get_child_observations` call per indicator returns every country and "
           "every year, so the whole sweep is a few hundred calls.", ""]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="sweep every enumerated base indicator, not just the usable ones")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--corpus", default=None,
                    help="corpus file for --all (default cache/corpus.json); pass "
                         "cache/corpus-all.json to sweep the whole graph")
    ap.add_argument("--recheck", action="store_true",
                    help="re-run the checks over cached observations, fetching nothing")
    args = ap.parse_args()

    targets = load_targets(args.all, args.limit, args.corpus)
    scope = ("all 689 enumerated SDG base indicators" if args.all
             else f"the {len(targets)} indicators screened usable (GREEN/AMBER/RANK-ONLY)")

    done = {}
    if args.resume and STATE.exists():
        done = {r["dcid"]: r for r in json.loads(STATE.read_text())["results"]}
        print(f"resuming: {len(done)} already swept", file=sys.stderr)

    raw = json.loads(RAW.read_text()) if RAW.exists() else {}
    if args.recheck:
        done = {}
        targets = [t for t in targets if t["dcid"] in raw]
        print(f"rechecking {len(targets)} cached indicators, fetching nothing",
              file=sys.stderr)

    client = Client(pause=0.5)
    todo = [t for t in targets if t["dcid"] not in done]
    for i, t in enumerate(todo, 1):
        d = t["dcid"]
        try:
            done[d] = sweep_one(client, d, raw)
        except UNDCError as exc:
            done[d] = {"dcid": d, "indicator": t.get("name") or d,
                       "error": str(exc), "findings": []}
        r = done[d]
        print(f"  {i}/{len(todo)} {d:<44} {r.get('n_obs', 0):>6} obs "
              f"{r.get('n_places', 0):>4} places  {len(r['findings']):>4} findings"
              + (f"  ERROR {r['error'][:40]}" if r.get("error") else ""), file=sys.stderr)
        if i % 25 == 0:
            STATE.write_text(json.dumps({"results": list(done.values())}, indent=1))
            RAW.write_text(json.dumps(raw))

    results = [done[t["dcid"]] for t in targets if t["dcid"] in done]
    STATE.write_text(json.dumps({"results": results}, indent=1))
    RAW.write_text(json.dumps(raw))

    today = dt.date.today().isoformat()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    findings = [f for r in results for f in r["findings"]]
    (ARTIFACTS / f"smell-{today}.json").write_text(json.dumps(
        {"generated": today, "scope": scope,
         "indicators_checked": len([r for r in results if not r.get("error")]),
         "observations": sum(r.get("n_obs", 0) for r in results),
         "findings": findings}, indent=1))
    text = render(results, scope)
    (ARTIFACTS / f"smell-{today}.md").write_text(text)
    (ARTIFACTS / "smell-latest.md").write_text(text)

    by_check = {}
    for f in findings:
        by_check.setdefault(f["check"], []).append(f)
    print(f"\n{'check':<24}{'sev':<8}{'findings':>10}{'indicators':>12}")
    for c in sorted(by_check, key=lambda c: (["HIGH", "MEDIUM", "LOW"].index(SEVERITY[c]),
                                             -len(by_check[c]))):
        print(f"{c:<24}{SEVERITY[c]:<8}{len(by_check[c]):>10}"
              f"{len({f['dcid'] for f in by_check[c]}):>12}")
    print(f"\n{sum(r.get('n_obs', 0) for r in results):,} observations · "
          f"{len([r for r in results if not r.get('error')])} indicators · "
          f"{len(findings):,} findings")
    print(f"wrote docs/artifacts/smell-{today}.md")


if __name__ == "__main__":
    main()
