#!/usr/bin/env python3
"""Render the municipal readiness table from inventory.json.

Separate from analyze.py because that re-queries every portal; this only
formats what has already been measured.
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
        return {"portal_csv": "own (snapshot)", "portal_csv_series": "own (series)",
                "census": "ACS"}[c["population"]["module"]]
    return "—"


muni = [r for r in rows if r.get("above_0.55") is not None]
muni.sort(key=lambda r: (-r["above_0.55"], -(r["datasets"] or 0)))
today = dt.date.today().isoformat()

md = ["---", "layout: default", f"title: Municipal readiness — {today}", "---", "",
      f"# Municipal portal readiness — {today}", "",
      "Which cities are worth starting a crosswalk on. Three gates: a reachable portal, "
      "indicators the matcher can find, and a population denominator.", "",
      "> **What the match column is not.** *≥0.55* counts UN indicators whose best match in "
      "that catalog clears a fixed similarity bar. It is a measure of **how much is worth "
      "reviewing**, not of quality — hand-reading candidate lists puts precision near half, and "
      "under [spec v0.1](../spec/) a grade is a human judgment regardless. NYC, the one city "
      "with hand-verified pairs, scores middling here, which is the clearest evidence that this "
      "column does not rank crosswalk success.", "",
      "> An earlier version of this table used each catalog's own calibrated cutoff. That keeps "
      "the top ~20% by construction, so **28 cities tied at exactly 12** and the column carried "
      "no information. Per-catalog calibration is right for bounding one city's worksheet and "
      "wrong for comparing cities.", "",
      f"**{len(muni)} municipal portals scored.**", "",
      "| Portal | Lang | Datasets | Best | ≥0.55 | ≥0.50 | Denominator |",
      "|---|---|---:|---:|---:|---:|---|"]
for r in muni:
    md.append(f"| [{r['portal']}]({r['url']}) | {r.get('match_language','?')} | "
              f"{r['datasets']:,} | {r['best']:.2f} | **{r['above_0.55']}** | "
              f"{r['above_0.5']} | {denom(r['portal'])} |")
md += ["", "## Reading it", "",
       "- **Catalog size does not predict potential.** Bolzano has 930 datasets and 19 indicators "
       "above 0.55; Milan has 2,602 and 4.",
       "- **Four of the top six are non-English.** Before the multilingual model these returned "
       "zero candidates.",
       "- **A denominator is the other gate.** A city with 19 candidates and no population source "
       "still cannot chart a rate — most SDG indicators are per 100,000.", ""]
out = ROOT / "docs/artifacts"
(out / f"readiness-{today}.md").write_text("\n".join(md))
(out / "readiness-latest.md").write_text("\n".join(md))
print(f"wrote docs/artifacts/readiness-{today}.md ({len(muni)} portals)")
