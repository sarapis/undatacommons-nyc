#!/usr/bin/env python3
"""How many UN indicators does each municipal portal plausibly hold?

Runs the bootstrapper's matching stage across every municipal portal in the
inventory and records the candidate count, so the table says which cities are
worth starting on rather than only how big they are.

WHAT THE COLUMN MEANS. A candidate is a dataset the matcher proposes for a UN
indicator, above that catalog's own calibrated cutoff. It is NOT a verified
match: hand-reading candidate lists puts precision around half, and under
comparability spec v0.1 a grade is a human judgment anyway. Read the number as
"roughly this much to review", never as "this many comparisons exist".

    python3 portals/matchable.py [--limit-indicators 80] [--max-datasets 2000]

Updates portals/inventory.json in place and rewrites the published table.
"""

import argparse
import json
import pathlib
import sys
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "probe"))

import embed                      # noqa: E402
import scope                      # noqa: E402
from portal import Portal, PortalError   # noqa: E402

INVENTORY = HERE / "inventory.json"
SCREENED = ROOT / "probe" / "cache" / "screened.json"
KEEP_FRACTION, ABSOLUTE_FLOOR = 0.20, 0.45

# The catalog's language decides the embedding model. Inferred from the TLD,
# which is crude but right far more often than assuming English.
TLD_LANG = {"es": "es", "mx": "es", "ar": "es", "cl": "es", "co": "es", "uy": "es",
            "it": "it", "br": "pt", "pt": "pt", "fr": "fr", "de": "de", "at": "de",
            "ch": "de", "nl": "nl", "dk": "da", "se": "sv", "no": "no", "fi": "fi",
            "gr": "el", "ua": "uk", "hr": "hr", "be": "nl", "cz": "cs", "pl": "pl"}


def language_for(host):
    tld = host.rsplit(".", 1)[-1].lower()
    return TLD_LANG.get(tld, "en")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-indicators", type=int, default=80)
    ap.add_argument("--max-datasets", type=int, default=2000)
    a = ap.parse_args()

    inv = json.loads(INVENTORY.read_text())
    rows = inv["rows"]
    muni = [r for r in rows if r.get("datasets") and r["level"] in ("city", "city-or-region")]
    muni.sort(key=lambda r: -(r["datasets"] or 0))

    indicators = [r for r in json.loads(SCREENED.read_text())["indicators"]
                  if r.get("grade") in ("GREEN", "AMBER", "RANK-ONLY")]
    indicators.sort(key=lambda r: -(r.get("panel_coverage") or 0))
    scoper = scope.Scoper()
    indicators = [r for r in indicators
                  if scoper.is_city(r.get("name"), scope.THRESHOLD)][:a.limit_indicators]
    print(f"{len(muni)} municipal portals · {len(indicators)} indicators", file=sys.stderr)

    by_portal = {r["portal"]: r for r in rows}
    for i, r in enumerate(muni, 1):
        host = r["portal"]
        lang = language_for(host)
        key = "inv-" + host.replace(".", "-")
        try:
            city = {"key": key, "name": host, "platform": r["platform"],
                    "domain": host if r["platform"] == "socrata" else r["url"]}
            catalog = Portal(city).catalog(limit=a.max_datasets)
            if not catalog:
                raise PortalError("empty catalog")
            index = embed.Index(datasets=catalog, cache_key=key, language=lang)
            tops = []
            for ind in indicators:
                hits = index.search(ind.get("name") or "", k=1)
                if hits:
                    tops.append(hits[0]["score"])
            tops.sort(reverse=True)
            cut = max(tops[max(0, int(len(tops) * KEEP_FRACTION) - 1)], ABSOLUTE_FLOOR) \
                if tops else ABSOLUTE_FLOOR
            n = sum(1 for t in tops if t >= cut)
            by_portal[host].update({"candidates": n, "catalog_sampled": len(catalog),
                                    "match_language": lang, "cutoff": round(cut, 3)})
            print(f"  [{i}/{len(muni)}] {host:<36} {len(catalog):>5} sets · "
                  f"{n:>3} candidates · {lang}", file=sys.stderr)
        except Exception as exc:                          # noqa: BLE001
            by_portal[host]["candidates_error"] = f"{type(exc).__name__}"
            print(f"  [{i}/{len(muni)}] {host:<36} FAILED {type(exc).__name__}",
                  file=sys.stderr)

    INVENTORY.write_text(json.dumps(inv, indent=1))
    done = [r for r in muni if r.get("candidates") is not None]
    print(f"\nscored {len(done)} of {len(muni)} municipal portals")


if __name__ == "__main__":
    main()
