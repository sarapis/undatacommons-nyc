#!/usr/bin/env python3
"""Population denominators, per city, from a cited source.

Most SDG indicators are rates per 100,000, so a chart needs a denominator, and a
wrong denominator produces a rate that looks exactly like a right one. Every
source here is named in cities/registry.json and resolved by a declared method.

WHY NOT ONE INTERNATIONAL SOURCE. Eurostat's Urban Audit (urb_cpop1) looks like
the obvious answer for Europe and is wrong for this purpose: it publishes
**greater cities**, not municipalities. Madrid's greater city is 5,115,272 while
the city's own padrón counts 3,520,396 -- a 45% inflation that would push every
Madrid rate about 31% too low, silently. Milan is worse: 3.58M greater city
against roughly 1.37M for the comune.

So denominators come from the city's own statistical publication wherever
possible. That also gives the numerator and denominator the same publisher,
which is better provenance than mixing sources.

Resolvers:
  census      US Census ACS 1-year, by place FIPS (annual, places >= ~65k)
  portal_csv  a CSV on the city's own portal, summing declared columns
"""

import csv
import io
import json
import pathlib
import ssl
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "probe"))


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


class PopulationError(RuntimeError):
    pass


def _census(city, years):
    import census as census_mod
    spec = city["population"]
    if spec.get("place") and spec.get("state"):
        return census_mod.population_for(spec["state"], spec["place"], years)
    pops, gaps = census_mod.nyc_population(years)       # NYC's original path
    return pops, gaps


def _portal_csv(city, years):
    """Sum declared columns of a CSV published on the city's own portal."""
    spec = city["population"]
    base = city["domain"].rstrip("/")
    meta_url = f"{base}/api/3/action/package_show?id={urllib.parse.quote(spec['dataset'])}"
    with urllib.request.urlopen(meta_url, timeout=90, context=_ctx()) as r:
        pkg = json.loads(r.read().decode())["result"]
    url = next((res["url"] for res in pkg.get("resources", [])
                if (res.get("format") or "").upper() == spec.get("format", "CSV")), None)
    if not url:
        raise PopulationError(f"no {spec.get('format','CSV')} resource on {spec['dataset']}")

    req = urllib.request.Request(url, headers={"User-Agent": "undatacommons-nyc"})
    with urllib.request.urlopen(req, timeout=300, context=_ctx()) as r:
        raw = r.read().decode(spec.get("encoding", "utf-8-sig"), errors="replace")

    total = 0
    for row in csv.DictReader(io.StringIO(raw), delimiter=spec.get("delimiter", ",")):
        for col in spec["sum_columns"]:
            v = (row.get(col) or "").strip()
            if v.isdigit():
                total += int(v)
    if not total:
        raise PopulationError(f"summed to zero; check sum_columns for {city['key']}")

    # A single snapshot, not a series: the same figure is returned for every
    # year requested, and the caller is told so rather than left to assume.
    return {y: total for y in years}, {"snapshot": True,
                                       "as_of": spec.get("as_of"),
                                       "source": spec["source"]}


def _portal_csv_series(city, years):
    """An annual series from a CSV on the city's own portal: year column + value column.

    Better than a snapshot -- it supports trends, not just levels. Milan's
    'Popolazione calcolata' runs 1880-2025 (ISTAT to 2002, then the city's own
    anagrafe), which is both authoritative and same-publisher for the years that
    matter.
    """
    spec = city["population"]
    base = city["domain"].rstrip("/")
    meta_url = f"{base}/api/3/action/package_show?id={urllib.parse.quote(spec['dataset'])}"
    with urllib.request.urlopen(meta_url, timeout=90, context=_ctx()) as r:
        pkg = json.loads(r.read().decode())["result"]
    url = next((res["url"] for res in pkg.get("resources", [])
                if (res.get("format") or "").upper() == spec.get("format", "CSV")), None)
    if not url:
        raise PopulationError(f"no {spec.get('format','CSV')} resource on {spec['dataset']}")

    req = urllib.request.Request(url, headers={"User-Agent": "undatacommons-nyc"})
    with urllib.request.urlopen(req, timeout=300, context=_ctx()) as r:
        raw = r.read().decode(spec.get("encoding", "utf-8-sig"), errors="replace")

    series = {}
    for row in csv.DictReader(io.StringIO(raw), delimiter=spec.get("delimiter", ",")):
        y = (row.get(spec["year_column"]) or "").strip()[:4]
        v = (row.get(spec["value_column"]) or "").strip().replace(".", "").replace(",", "")
        if y.isdigit() and v.isdigit():
            series[int(y)] = int(v)
    if not series:
        raise PopulationError(f"parsed no rows; check year/value columns for {city['key']}")

    got = {y: series[y] for y in years if y in series}
    missing = sorted(set(years) - set(got))
    return got, {"snapshot": False, "source": spec["source"],
                 "covers": f"{min(series)}-{max(series)}",
                 "years_missing": missing}


RESOLVERS = {"census": _census, "portal_csv": _portal_csv,
             "portal_csv_series": _portal_csv_series}


def resolve(city, years):
    """(populations by year, metadata). Raises if the city declares no source."""
    spec = city.get("population")
    if not spec:
        raise PopulationError(
            f"{city['key']} declares no population source. Rate-based indicators "
            f"cannot be completed until one is recorded in cities/registry.json "
            f"with a citation -- an uncited denominator is how a rate becomes fiction.")
    fn = RESOLVERS.get(spec.get("module"))
    if not fn:
        raise PopulationError(f"unknown population module {spec.get('module')!r}")
    return fn(city, list(years))


if __name__ == "__main__":
    reg = json.loads((ROOT / "cities" / "registry.json").read_text())["cities"]
    key = sys.argv[1] if len(sys.argv) > 1 else "madrid"
    city = next(c for c in reg if c["key"] == key)
    pops, meta = resolve(city, [2024])
    print(f"{city['name']}: {list(pops.values())[0]:,}")
    print(f"   {meta}")
