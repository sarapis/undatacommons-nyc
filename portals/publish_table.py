#!/usr/bin/env python3
"""Render one combined municipal table: identity, size, matchability, denominator.

Replaces the separate inventory and readiness tables -- they were keyed by the
same portals and split the same story across two pages.
"""
import datetime as dt, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = json.loads((ROOT / "portals/inventory.json").read_text())["rows"]
den = json.loads((ROOT / "cities/denominators.json").read_text())
ready = {r["portal"] for r in den["ready"]}
reg = {c["domain"].replace("https://", "").replace("http://", "").rstrip("/"): c
       for c in json.loads((ROOT / "cities/registry.json").read_text())["cities"]}


def denom(h):
    if h in ready:
        return "ACS"
    c = reg.get(h)
    if c and c.get("population"):
        return {"portal_csv": "own · snapshot", "portal_csv_series": "own · series",
                "census": "ACS"}[c["population"]["module"]]
    return "—"


muni = [r for r in rows if r["level"] in ("city", "city-or-region") and r.get("datasets")]
muni.sort(key=lambda r: (-(r.get("above_0.55") if r.get("above_0.55") is not None else -1),
                         -(r["datasets"] or 0)))
today = dt.date.today().isoformat()
scored = [r for r in muni if r.get("above_0.55") is not None]
with_den = [r for r in muni if denom(r["portal"]) != "—"]

md = ["---", "layout: default", f"title: Municipal portals — {today}", "---", "",
      f"# Municipal open data portals — {today}", "",
      f"**{len(muni)} city and regional portals**, holding "
      f"{sum(r['datasets'] for r in muni):,} datasets. {len(scored)} scored for matchable UN "
      f"indicators; {len(with_den)} have a population denominator wired.", "",
      "Three gates decide whether a city can produce a chart: a reachable portal, indicators the "
      "matcher can find, and a denominator. This table shows all three.", "",
      "> **≥0.55 is review volume, not quality.** It counts UN indicators whose best match in "
      "that catalog clears a fixed similarity bar. Hand-reading candidate lists puts precision "
      "near half, and under [spec v0.1](../spec/) a grade is a human judgment regardless. NYC — "
      "the only city with hand-verified pairs — scores middling, which is the clearest evidence "
      "this column does not rank crosswalk success.", "",
      "> **City and country are derived**, from an ACS place match, the project registry, a CKAN "
      "title, the domain, or a hand override where none of those work. The source is recorded "
      "per row in `portals/inventory.json` so a wrong one can be traced.", "",
      "| City | Country | Portal | Plat | Lang | Datasets | Best | ≥0.55 | ≥0.50 | Denominator |",
      "|---|---|---|---|---|---:|---:|---:|---:|---|"]
for r in muni:
    b = f"{r['best']:.2f}" if r.get("best") is not None else "—"
    a55 = r.get("above_0.55"); a50 = r.get("above_0.5")
    a55 = "**" + str(a55) + "**" if a55 is not None else "—"
    a50 = str(a50) if a50 is not None else "—"
    md.append(f"| {r.get('city') or '?'} | {r.get('country_name') or '?'} | "
              f"[{r['portal']}]({r['url']}) | {r['platform']} | "
              f"{r.get('match_language','?')} | {r['datasets']:,} | {b} | {a55} | {a50} | "
              f"{denom(r['portal'])} |")
md += ["", "## Reading it", "",
       "- **Catalog size does not predict potential.** Bolzano has 930 datasets and 19 indicators "
       "above 0.55; Milan has 2,602 and 4.",
       "- **Four of the top six are non-English**, and returned zero candidates before a "
       "multilingual embedding model was added.",
       "- **The denominator is the binding gate.** Most SDG indicators are rates per 100,000, so "
       "a city with 19 candidates and no population source still cannot chart one. 27 US cities "
       "resolve via Census ACS; Madrid and Milan are wired from their own statistical "
       "publications; the rest need one.", ""]
out = ROOT / "docs/artifacts"
(out / f"municipal-{today}.md").write_text("\n".join(md))
(out / "municipal-latest.md").write_text("\n".join(md))
print(f"wrote docs/artifacts/municipal-{today}.md — {len(muni)} portals")
