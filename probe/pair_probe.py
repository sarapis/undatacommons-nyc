#!/usr/bin/env python3
"""Pair probe: verify both sides of each crosswalk entry, not just the UN side.

The coverage probe grades UN variables in isolation. That is half a bridge. This
walks probe/crosswalk.json, resolves the UN series AND runs the declared NYC
SoQL, then reports whether the pair can actually be charted -- overlapping years,
agreeing units, and no blockers.

It does NOT assign comparability grades. Those are human judgments recorded in
crosswalk.json; the probe's job is to catch a mapping that has silently stopped
resolving, not to decide what is comparable.

Usage:  python3 probe/pair_probe.py
Writes docs/artifacts/crosswalk-<date>.{json,md}.
"""

import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from undc import Client, UNDCError          # noqa: E402
import nyc                                   # noqa: E402
import census                                 # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "docs" / "artifacts"

# Unit DCIDs the UN side uses, mapped to what we would call them locally. Used
# only to flag an obvious mismatch; a match here is necessary, not sufficient.
UNIT_EQUIV = {
    "RATIO_WEIGHT_MICROGR_PER_VOL_M3": {"mcg/m3", "ug/m3"},
    "RATIO_COUNT_PER_100000_COUNT_POP": {"per 100k"},
    "RATIO_COUNT_PERCENT": {"percent", "%"},
    "PERCENT": {"percent", "%"},
    # Not every variable reports a UNIT_MEASURE DCID; some return a bare name.
    "Percent": {"percent", "%"},
}


def un_side(client, spec):
    try:
        o = client.get_observations(spec["dcid"], spec["place"], date="all")
    except UNDCError as exc:
        return {"error": str(exc)}
    rows = (o.get("data") or {}).get("rows") or []
    years = sorted({int(str(r[1])[:4]) for r in rows if str(r[1])[:4].isdigit()})
    src = o.get("sourceMetadata") or {}
    unit = (src.get("unit") or "").split("UNIT_MEASURE-")[-1]
    return {
        "dcid": spec["dcid"], "name": (o.get("variable") or {}).get("name"),
        "n_obs": len(rows), "years": years, "unit": unit,
        "provenance": src.get("provenanceUrl"),
        "values": {str(r[1])[:4]: r[2] for r in rows},
    }


def nyc_side(spec):
    out = {"dataset": spec["dataset"], "declared_unit": spec.get("unit")}
    try:
        meta = nyc.metadata(spec["dataset"])
        out.update({"name": meta["name"], "updated_at": meta["updated_at"],
                    "archived": meta["archived"]})
    except nyc.NYCError as exc:
        out["error"] = f"metadata: {exc}"
        return out
    try:
        rows = nyc.query(spec["dataset"], spec["soql"])
    except nyc.NYCError as exc:
        out["error"] = f"query: {exc}"
        return out

    yf, vf = spec.get("year_field", "yr"), spec.get("value_field", "value")
    values = {}
    for r in rows:
        y = str(r.get(yf, ""))[:4]
        if y.isdigit() and r.get(vf) is not None:
            values[y] = float(r[vf])
    out["n_obs"] = len(values)
    out["years"] = sorted(int(y) for y in values)
    out["values"] = values
    return out


def apply_denominator(pair, ny):
    """Convert a NYC count series into a rate when the pair declares one.

    Years with no denominator are DROPPED, not estimated. ACS 1-year has no 2020
    release, so 2020 simply has no rate -- and that is the honest rendering. An
    interpolated denominator yields a rate indistinguishable from a measured one.
    """
    spec = pair.get("denominator")
    if not spec or ny.get("error") or not ny.get("values"):
        return ny

    years = [int(y) for y in ny["values"]]
    try:
        pop, gaps = census.nyc_population(range(min(years), max(years) + 1))
    except census.CensusError as exc:
        ny["denominator_error"] = str(exc)
        return ny

    per = spec.get("per", 100000)
    rates, dropped = {}, []
    for y, v in ny["values"].items():
        if int(y) in pop:
            rates[y] = v / pop[int(y)] * per
        else:
            dropped.append(int(y))

    ny["raw_counts"] = ny["values"]
    ny["values"] = rates
    ny["years"] = sorted(int(y) for y in rates)
    ny["n_obs"] = len(rates)
    ny["declared_unit"] = spec.get("unit", "per 100k")
    ny["denominator"] = {"source": spec.get("source", "ACS 1-year B01003_001E"),
                         "per": per, "years_dropped_no_denominator": sorted(dropped)}
    return ny


def assess(pair, un, ny):
    """Mechanical checks only. Comparability stays a human call."""
    blockers = []
    if un.get("error"):
        blockers.append(f"UN side did not resolve: {un['error']}")
    if ny.get("error"):
        blockers.append(f"NYC side did not resolve: {ny['error']}")
    if ny.get("archived"):
        blockers.append(f"NYC dataset is ARCHIVED ({ny.get('name')})")
    if pair.get("requires_denominator") and not ny.get("denominator"):
        blockers.append("needs a population denominator before the two can share an axis")
    if ny.get("denominator_error"):
        blockers.append(f"denominator unavailable: {ny['denominator_error']}")

    un_years, ny_years = set(un.get("years") or []), set(ny.get("years") or [])
    overlap = sorted(un_years & ny_years)
    if not overlap and not blockers:
        blockers.append("no overlapping years")

    un_unit, ny_unit = un.get("unit") or "", (ny.get("declared_unit") or "").lower()
    accepted = UNIT_EQUIV.get(un_unit)
    if accepted is None:
        unit_check = f"unmapped UN unit `{un_unit}` - check by hand"
    elif ny_unit in accepted:
        unit_check = "units agree"
    else:
        unit_check = f"UNIT MISMATCH: UN `{un_unit}` vs NYC `{ny_unit}`"
        blockers.append(unit_check)

    return {"overlap_years": overlap, "unit_check": unit_check,
            "blockers": blockers, "chartable": not blockers}


def main():
    spec = json.loads((ROOT / "probe" / "crosswalk.json").read_text())
    client = Client()
    out = []
    for pair in spec["pairs"]:
        print(f"-> {pair['id']}", file=sys.stderr)
        un = un_side(client, pair["un"])
        ny = apply_denominator(pair, nyc_side(pair["nyc"]))
        out.append({"pair": pair, "un": un, "nyc": ny,
                    "assessment": assess(pair, un, ny)})

    today = dt.date.today().isoformat()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / f"crosswalk-{today}.json").write_text(
        json.dumps({"generated": today, "pairs": out}, indent=2))

    md = [f"---", "layout: default", f"title: Crosswalk status — {today}", "---", "",
          f"# Crosswalk status — {today}", "",
          "Both sides of every mapping, verified. The grade in each entry is a **human**",
          "judgment recorded in `probe/crosswalk.json`; this page verifies that the mapping",
          "still resolves and that the units agree.", "",
          "| Pair | SDG | Grade | Chartable | Overlap | Units | Blockers |",
          "|---|---|---|---|---|---|---|"]
    for r in out:
        p, a = r["pair"], r["assessment"]
        ov = f"{a['overlap_years'][0]}–{a['overlap_years'][-1]}" if a["overlap_years"] else "—"
        md.append(f"| {p['label']} | {p['sdg']} | {p['grade']} | "
                  f"{'yes' if a['chartable'] else 'NO'} | {ov} | {a['unit_check']} | "
                  f"{'; '.join(a['blockers']) or '—'} |")

    md += ["", "## Detail", ""]
    for r in out:
        p, un, ny, a = r["pair"], r["un"], r["nyc"], r["assessment"]
        md += [f"### {p['label']} (SDG {p['sdg']}) — **{p['grade']}**", "",
               f"*{p['reason']}*", "",
               f"- **UN** `{p['un']['dcid']}` — {un.get('n_obs', 0)} obs"
               + (f", {un['years'][0]}–{un['years'][-1]}" if un.get("years") else "")
               + f", unit `{un.get('unit')}`, source {un.get('provenance') or '—'}",
               f"- **NYC** `{p['nyc']['dataset']}` {ny.get('name', '')} — "
               f"{ny.get('n_obs', 0)} obs"
               + (f", {ny['years'][0]}–{ny['years'][-1]}" if ny.get("years") else "")
               + f", updated {ny.get('updated_at', '—')}",
               *([f"- **Denominator** {ny['denominator']['source']}, per "
                  f"{ny['denominator']['per']:,}"
                  + (f" — no denominator for "
                     f"{', '.join(str(x) for x in ny['denominator']['years_dropped_no_denominator'])}, "
                     f"those years carry no rate"
                     if ny['denominator']['years_dropped_no_denominator'] else "")]
                 if ny.get("denominator") else []),
               f"- Overlap: {a['overlap_years'][0] if a['overlap_years'] else '—'}"
               + (f"–{a['overlap_years'][-1]}" if a["overlap_years"] else "")
               + f" · {a['unit_check']}", ""]
        if a["blockers"]:
            md += ["  **Blockers:** " + "; ".join(a["blockers"]), ""]

    text = "\n".join(md)
    (ARTIFACTS / f"crosswalk-{today}.md").write_text(text)
    (ARTIFACTS / "crosswalk-latest.md").write_text(text)
    print(f"\nwrote docs/artifacts/crosswalk-{today}.md", file=sys.stderr)


if __name__ == "__main__":
    main()
