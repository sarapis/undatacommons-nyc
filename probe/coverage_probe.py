#!/usr/bin/env python3
"""Coverage probe: find out which UN indicators can actually carry a chart.

The motivating failure: SDG 3.6.1 (road traffic deaths) looks like a perfect
demo indicator and returns exactly ONE observation for the United States, in
2021. You cannot draw a trend through one point. This sweeps a candidate list
and grades each variable on whether it is chartable, so we choose indicators on
evidence instead of intuition.

Usage:
    python3 probe/coverage_probe.py                 # default candidate list
    python3 probe/coverage_probe.py --peers         # also probe peer countries
    python3 probe/coverage_probe.py --limit 5       # fewer results per topic

Writes docs/artifacts/coverage-<date>.{json,md}.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from undc import Client, GOVERNED_PREFIX, UNDCError  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "docs" / "artifacts"

# A variable needs this many observations before a trend line means anything.
CHARTABLE_MIN_OBS = 5
CHARTABLE_MIN_SPAN = 5
RECENT_SINCE = 2018

# WHO and similar agencies publish modelled estimates rather than administrative
# counts. That is not a defect, but putting one next to a city's own incident
# count is exactly the comparison that misleads, so we surface it.
ESTIMATE_HINTS = ("estimated", "estimate", "modelled", "modeled", "projected")


def grade(n_obs, span, latest_year):
    if n_obs <= 1:
        return "RED", "single point or none - no trend possible"
    if n_obs < CHARTABLE_MIN_OBS or span < CHARTABLE_MIN_SPAN:
        return "AMBER", f"{n_obs} points over {span}y - sparse, usable only as a level"
    if latest_year and latest_year < RECENT_SINCE:
        return "AMBER", f"latest point is {latest_year} - stale for an operations audience"
    return "GREEN", f"{n_obs} points over {span}y - chartable"


def probe_variable(client, dcid, place):
    """Fetch the full series for one variable and reduce it to a coverage row."""
    try:
        obs = client.get_observations(dcid, place, date="all")
    except UNDCError as exc:
        return {"dcid": dcid, "place": place, "error": str(exc), "grade": "ERROR"}

    rows = (obs.get("data") or {}).get("rows") or []
    years = sorted({int(str(r[1])[:4]) for r in rows if len(r) > 1 and str(r[1])[:4].isdigit()})
    src = obs.get("sourceMetadata") or {}
    name = (obs.get("variable") or {}).get("name") or ""

    n_obs = len(rows)
    span = (years[-1] - years[0] + 1) if years else 0
    latest = years[-1] if years else None
    g, why = grade(n_obs, span, latest)

    return {
        "dcid": dcid,
        "name": name,
        "place": place,
        "n_obs": n_obs,
        "first_year": years[0] if years else None,
        "latest_year": latest,
        "span_years": span,
        "annual": bool(years) and len(years) == span,
        "unit": src.get("unit"),
        "observation_period": src.get("observationPeriod"),
        "provenance_url": src.get("provenanceUrl"),
        # QA flags -- these feed the comparability grader later
        "modelled_estimate": any(h in name.lower() for h in ESTIMATE_HINTS),
        "governed": dcid.startswith(GOVERNED_PREFIX),
        "grade": g,
        "grade_reason": why,
    }


def run(candidates, limit, include_peers):
    client = Client()
    places = list(candidates["places"])
    if include_peers:
        places += candidates.get("peer_places", [])

    results = []
    for topic in candidates["topics"]:
        print(f"-> {topic['id']:<12} {topic['label']}", file=sys.stderr)
        try:
            found = client.search_indicators(topic["query"], places=places, limit=limit)
        except UNDCError as exc:
            print(f"   search failed: {exc}", file=sys.stderr)
            results.append({"topic": topic, "variables": [], "search_error": str(exc)})
            continue

        # search_indicators reports, per variable, which of our places have data.
        # A variable with an empty placesWithData is one we cannot use at all.
        variables = found.get("variables") or []
        names = found.get("dcidNameMappings") or {}
        rows = []
        for var in variables:
            dcid = var.get("dcid")
            with_data = var.get("placesWithData") or []
            if not with_data:
                rows.append({
                    "dcid": dcid, "name": names.get(dcid, ""), "place": None,
                    "n_obs": 0, "grade": "RED",
                    "grade_reason": "no data for any probed place",
                    "governed": bool(dcid) and dcid.startswith(GOVERNED_PREFIX),
                })
                continue
            for place in with_data:
                rows.append(probe_variable(client, dcid, place))

        results.append({"topic": topic, "variables": rows,
                        "n_candidates": len(variables)})
    return results


def to_markdown(results, places):
    today = dt.date.today().isoformat()
    out = [
        "---",
        "layout: default",
        f"title: Indicator coverage — {today}",
        "---",
        "",
        f"# Indicator coverage probe — {today}",
        "",
        f"Places probed: {', '.join(places)}",
        "",
        "Grades: **GREEN** chartable · **AMBER** sparse, usable as a level only · "
        "**RED** unusable for a trend.",
        "",
        "| Grade | Topic | Variable | DCID | Obs | Years | Modelled | Source |",
        "|---|---|---|---|---:|---|---|---|",
    ]
    order = {"GREEN": 0, "AMBER": 1, "RED": 2, "ERROR": 3}
    flat = []
    for entry in results:
        for row in entry["variables"]:
            flat.append((entry["topic"], row))
    flat.sort(key=lambda t: (order.get(t[1].get("grade"), 9), t[0]["id"]))

    for topic, row in flat:
        years = (f"{row.get('first_year')}–{row.get('latest_year')}"
                 if row.get("first_year") else "—")
        src = (row.get("provenance_url") or "").replace("https://", "")
        out.append(
            f"| {row.get('grade')} | {topic['id']} | {row.get('name') or '—'} | "
            f"`{row.get('dcid')}` | {row.get('n_obs', 0)} | {years} | "
            f"{'yes' if row.get('modelled_estimate') else ''} | {src} |"
        )

    counts = {}
    for _, row in flat:
        counts[row.get("grade")] = counts.get(row.get("grade"), 0) + 1
    out += ["", "## Summary", ""]
    for g in ("GREEN", "AMBER", "RED", "ERROR"):
        if counts.get(g):
            out.append(f"- **{g}**: {counts[g]}")
    out += [
        "",
        "## How to read this",
        "",
        "A RED row is not a broken query — it is the platform telling us the indicator",
        "cannot support the chart we had in mind. Choose demo indicators from GREEN.",
        "A `modelled` yes means the UN figure is an estimate, not a count; pairing one",
        "with a NYC administrative count needs an explicit caveat on the chart.",
        "",
        "Regenerate with `python3 probe/coverage_probe.py`.",
    ]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", default=str(ROOT / "probe" / "candidates.json"))
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--peers", action="store_true", help="also probe peer countries")
    args = ap.parse_args()

    candidates = json.loads(pathlib.Path(args.candidates).read_text())
    places = list(candidates["places"]) + (
        candidates.get("peer_places", []) if args.peers else [])

    results = run(candidates, args.limit, args.peers)

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    (ARTIFACTS / f"coverage-{today}.json").write_text(
        json.dumps({"generated": today, "places": places, "results": results}, indent=2))
    md = to_markdown(results, places)
    (ARTIFACTS / f"coverage-{today}.md").write_text(md)
    (ARTIFACTS / "coverage-latest.md").write_text(md)
    print(f"\nwrote docs/artifacts/coverage-{today}.md", file=sys.stderr)


if __name__ == "__main__":
    main()
