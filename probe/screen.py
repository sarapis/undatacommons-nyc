#!/usr/bin/env python3
"""Stage 2 — screen base indicators for US coverage worth crosswalking.

Uses get_variable_metadata, which accepts a LIST of variables and returns
obsCount, dateRange, unit and entity coverage for each. That is what makes
corpus-scale screening feasible: one call per batch instead of one
get_observations per indicator.

Grading matches the coverage probe -- a trend needs enough points over enough
years, recently enough to interest an operations audience.

Usage:  python3 probe/screen.py [--limit N] [--resume]
Reads probe/cache/corpus.json, writes probe/cache/screened.json.
"""

import argparse
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from undc import Client, UNDCError  # noqa: E402

CACHE = pathlib.Path(__file__).resolve().parent / "cache"
CORPUS, SCREENED = CACHE / "corpus.json", CACHE / "screened.json"
US = "country/USA"

MIN_OBS, MIN_SPAN, RECENT_SINCE = 5, 5, 2015

# get_variable_metadata silently truncates above ~10 variables per call: it
# returns status None and an EMPTY variables map rather than an error. An
# earlier version of this script used 40 and cheerfully reported "689/689
# screened" having recorded 9. Never raise this without re-testing, and never
# trust a batch result without verify_batch below.
BATCH = 10


def grade(n_obs, span, latest):
    if n_obs <= 1:
        return "RED"
    if n_obs < MIN_OBS or span < MIN_SPAN:
        return "AMBER"
    if latest and latest < RECENT_SINCE:
        return "AMBER"
    return "GREEN"


def fetch_metadata(client, dcids, attempt=1):
    """Fetch metadata, refusing to accept a silently truncated response.

    A short or empty result is treated as failure and retried in halves, so a
    batch-size regression shows up as missing rows we can see rather than as a
    confident undercount.
    """
    try:
        r = client.call_tool("get_variable_metadata",
                             {"variable_dcids": dcids, "entity_dcids": [US]})
    except UNDCError as exc:
        if "403" in str(exc) and attempt <= 4:
            wait = 5 * attempt
            print(f"  rate limited; backing off {wait}s", file=sys.stderr)
            time.sleep(wait)
            return fetch_metadata(client, dcids, attempt + 1)
        print(f"  ! batch failed: {exc}", file=sys.stderr)
        return {}

    got = r.get("variables") or {}
    if len(got) < len(dcids):
        if len(dcids) == 1:
            return got                      # genuinely absent from the graph
        mid = len(dcids) // 2
        print(f"  short response ({len(got)}/{len(dcids)}); splitting",
              file=sys.stderr)
        return {**fetch_metadata(client, dcids[:mid]),
                **fetch_metadata(client, dcids[mid:])}
    return got


def screen(client, dcids):
    """Return one row per indicator, choosing its best facet for the US."""
    rows = []
    for dcid, meta in fetch_metadata(client, dcids).items():
        facets = meta.get("facets") or []
        # Keep only facets that actually cover the US, then take the richest.
        usable = [f for f in facets
                  if US in ((f.get("scope") or {}).get("entityCoverage") or [])]
        if not usable:
            rows.append({"dcid": dcid, "name": meta.get("name"), "n_obs": 0,
                         "grade": "NO-US-DATA"})
            continue
        best = max(usable, key=lambda f: f.get("obsCount") or 0)
        dr = best.get("dateRange") or {}
        start, end = str(dr.get("start", ""))[:4], str(dr.get("end", ""))[:4]
        first = int(start) if start.isdigit() else None
        latest = int(end) if end.isdigit() else None
        span = (latest - first + 1) if (first and latest) else 0
        n = best.get("obsCount") or 0
        props = best.get("properties") or {}
        rows.append({
            "dcid": dcid, "name": meta.get("name"), "n_obs": n,
            "first_year": first, "latest_year": latest, "span_years": span,
            "unit": (props.get("unit") or "").split("UNIT_MEASURE-")[-1],
            "observation_period": props.get("observationPeriod"),
            "provenance": best.get("provenanceId"),
            "grade": grade(n, span, latest),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="screen only the first N")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    corpus = json.loads(CORPUS.read_text())
    bases = sorted(corpus["bases"])
    if args.limit:
        bases = bases[:args.limit]

    done = {}
    if args.resume and SCREENED.exists():
        done = {r["dcid"]: r for r in json.loads(SCREENED.read_text())["indicators"]}
        print(f"resuming: {len(done)} already screened", file=sys.stderr)
    todo = [b for b in bases if b not in done]

    client = Client(pause=0.6)   # 403s appear if we push harder than this
    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        for row in screen(client, chunk):
            done[row["dcid"]] = row
        print(f"  screened {min(i + BATCH, len(todo))}/{len(todo)}", file=sys.stderr)
        if i % (BATCH * 10) == 0:
            SCREENED.write_text(json.dumps(
                {"screened": len(done), "indicators": list(done.values())}, indent=1))

    missing = [b for b in bases if b not in done]
    if missing:
        print(f"\n  WARNING: {len(missing)} indicator(s) returned no metadata at all",
              file=sys.stderr)
    rows = list(done.values())
    counts = {}
    for r in rows:
        counts[r["grade"]] = counts.get(r["grade"], 0) + 1
    SCREENED.write_text(json.dumps(
        {"requested": len(bases), "screened": len(rows),
         "not_returned": missing, "grade_counts": counts,
         "indicators": rows}, indent=1))
    print(f"\nscreened {len(rows):,}")
    for g, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {g:<12} {n:,}")
    print(f"\nwrote {SCREENED}")


if __name__ == "__main__":
    main()
