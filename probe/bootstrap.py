#!/usr/bin/env python3
"""Bootstrap a crosswalk candidate list for any city in cities/registry.json.

WHAT THIS DOES NOT PRODUCE IS A CROSSWALK.

Under comparability spec v0.1 a grade is a human judgment, so a machine cannot
emit a conforming crosswalk by definition. This produces the *input* to grading:
for each UN indicator a city could plausibly report, the best-matching datasets
in that city's own catalog, ranked, for a local analyst to grade or reject.

    python3 probe/bootstrap.py --city boston
    python3 probe/bootstrap.py --city madrid --limit 60

Writes cities/<key>/candidates.json and a Markdown worksheet beside it.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from portal import Portal, PortalError   # noqa: E402
import embed                             # noqa: E402
import scope                             # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "cities" / "registry.json"
SCREENED = ROOT / "probe" / "cache" / "screened.json"

USABLE = ("GREEN", "AMBER", "RANK-ONLY")
MIN_SIMILARITY = 0.50


def load_city(key):
    reg = json.loads(REGISTRY.read_text())
    for c in reg["cities"]:
        if c["key"] == key:
            return c
    raise SystemExit(f"unknown city {key!r}. Known: "
                     + ", ".join(c["key"] for c in reg["cities"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", required=True)
    ap.add_argument("--limit", type=int, default=0, help="cap indicators probed")
    ap.add_argument("--catalog-limit", type=int, default=3000)
    a = ap.parse_args()

    city = load_city(a.city)
    out_dir = ROOT / "cities" / city["key"]
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"-> {city['name']} ({city['platform']}, {city['domain']})", file=sys.stderr)
    portal = Portal(city)
    try:
        catalog = portal.catalog(limit=a.catalog_limit)
    except PortalError as exc:
        raise SystemExit(f"catalog fetch failed: {exc}")
    print(f"   {len(catalog)} datasets · model "
          f"{embed.model_for(city.get('language','en')).split('/')[-1]}", file=sys.stderr)

    with_cols = sum(1 for d in catalog if d.get("columns"))
    if not embed.available():
        raise SystemExit("model2vec required: pip3 install model2vec")

    index = embed.Index(datasets=catalog, cache_key=city["key"],
                        language=city.get("language", "en"))
    scoper = scope.Scoper()

    indicators = [r for r in json.loads(SCREENED.read_text())["indicators"]
                  if r.get("grade") in USABLE]
    indicators.sort(key=lambda r: -(r.get("panel_coverage") or 0))
    indicators = [r for r in indicators if scoper.is_city(r.get("name"), scope.THRESHOLD)]
    if a.limit:
        indicators = indicators[:a.limit]
    print(f"   {len(indicators)} city-scoped indicators to match", file=sys.stderr)

    results = []
    for ind in indicators:
        cands = [c for c in index.search(ind.get("name") or "", k=3)
                 if c["score"] >= MIN_SIMILARITY]
        if cands:
            results.append({
                "indicator": {"dcid": ind["dcid"], "name": ind.get("name"),
                              "grade_un_side": ind.get("grade"),
                              "panel_coverage": ind.get("panel_coverage")},
                "candidates": [{"id": c["id"], "name": c["name"],
                                "url": c.get("url"), "updated": c.get("updated"),
                                "similarity": c["score"]} for c in cands],
            })

    today = dt.date.today().isoformat()
    doc = {"generated": today, "city": city, "spec_version": "0.1",
           "is_crosswalk": False,
           "note": ("Candidates only. Under comparability spec v0.1 a grade is a human "
                    "judgment, so this is the input to grading, not a crosswalk. Nothing "
                    "here may be charted until a person grades it."),
           "catalog_size": len(catalog),
           "catalog_datasets_with_field_names": with_cols,
           "indicators_probed": len(indicators),
           "results": results}
    (out_dir / "candidates.json").write_text(json.dumps(doc, indent=1))

    md = ["# " + city["name"] + " — crosswalk candidates", "",
          f"Generated {today} · {city['platform']} · `{city['domain']}`", "",
          "**This is not a crosswalk.** A grade is a human judgment (comparability spec v0.1), "
          "so this is the worksheet a local analyst grades. Nothing here may be charted until "
          "someone does.", "",
          f"- catalog: **{len(catalog)}** datasets "
          f"({with_cols} publish field names — matching is weaker without them)",
          f"- indicators probed: **{len(indicators)}** (city-scoped, usable UN coverage)",
          f"- with at least one candidate above {MIN_SIMILARITY}: **{len(results)}**", ""]
    if not city.get("population"):
        md += ["> ⚠ **No sourced population denominator for this city.** Rate-based indicators "
               "(most SDG health and safety measures are per 100,000) cannot be completed until "
               "one is recorded in `cities/registry.json` with its source.", ""]
    md += ["| Sim | UN indicator | Candidate dataset | Grade (fill in) |",
           "|---|---|---|---|"]
    for r in sorted(results, key=lambda r: -r["candidates"][0]["similarity"])[:80]:
        i, c = r["indicator"], r["candidates"][0]
        md.append(f"| {c['similarity']:.2f} | {(i['name'] or '')[:52]} | "
                  f"[{(c['name'] or '')[:42]}]({c.get('url') or ''}) | |")
    md += ["", f"*{len(results)} rows; showing the top 80. "
           f"Regenerate with `python3 probe/bootstrap.py --city {city['key']}`.*", ""]
    (out_dir / "candidates.md").write_text("\n".join(md))

    print(f"\n{city['name']}: {len(catalog)} datasets, {len(results)} indicators with candidates")
    print(f"   field names published by {with_cols}/{len(catalog)} datasets")
    print(f"   wrote cities/{city['key']}/candidates.json + .md")


if __name__ == "__main__":
    main()
