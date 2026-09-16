#!/usr/bin/env python3
"""Fetch and cache the municipal catalogs, so they stop being refetched.

portals/matchable.py pulls every catalog live on each run, which is why
re-rendering the table was documented as expensive. The catalogs themselves are
a reusable asset -- 46 English city portals, ~12,000 datasets -- and nothing
else in the repo keeps them.

Usage: python3 probe/fetch_municipal.py [--limit-portals N] [--max-datasets N]
Writes probe/cache/municipal-catalogs.json (gitignored; regenerate with this).
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "probe"))
from portal import Portal, PortalError  # noqa: E402

INVENTORY = ROOT / "portals" / "inventory.json"
OUT = ROOT / "probe" / "cache" / "municipal-catalogs.json"

TLD_LANG = {"es": "es", "mx": "es", "ar": "es", "cl": "es", "co": "es", "uy": "es",
            "it": "it", "br": "pt", "pt": "pt", "fr": "fr", "de": "de", "at": "de",
            "ch": "de", "nl": "nl", "dk": "da", "se": "sv", "no": "no", "fi": "fi",
            "gr": "el", "ua": "uk", "hr": "hr", "be": "nl", "cz": "cs", "pl": "pl"}


def language_for(host):
    return TLD_LANG.get(host.rsplit(".", 1)[-1].lower(), "en")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-datasets", type=int, default=3000)
    ap.add_argument("--limit-portals", type=int, default=0)
    args = ap.parse_args()

    rows = [r for r in json.loads(INVENTORY.read_text())["rows"]
            if r.get("level") == "city"]
    rows.sort(key=lambda r: -(r.get("datasets") or 0))
    if args.limit_portals:
        rows = rows[:args.limit_portals]

    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    for i, r in enumerate(rows, 1):
        host = r["portal"]
        if host in out:
            print(f"  {i}/{len(rows)} {host} cached", file=sys.stderr)
            continue
        try:
            # Same key convention as portals/matchable.py, so the cached
            # inv-<host>_v2_vectors.npz files are reused rather than rebuilt.
            key = "inv-" + host.replace(".", "-")
            ds = Portal({"key": key, "name": host, "platform": r["platform"],
                         "domain": host if r["platform"] == "socrata" else r["url"]}
                        ).catalog(limit=args.max_datasets)
            out[host] = {"portal": host, "key": key, "city": r.get("city"),
                         "country": r.get("country_name") or r.get("country"),
                         "platform": r.get("platform"),
                         "language": language_for(host), "datasets": ds}
            print(f"  {i}/{len(rows)} {host:<40}{len(ds):>6} datasets", file=sys.stderr)
        except (PortalError, Exception) as exc:              # noqa: BLE001
            out[host] = {"portal": host, "city": r.get("city"), "error": str(exc)[:200],
                         "datasets": []}
            print(f"  {i}/{len(rows)} {host:<40}ERROR {str(exc)[:60]}", file=sys.stderr)
        if i % 5 == 0:
            OUT.write_text(json.dumps(out))
    OUT.write_text(json.dumps(out))

    ok = [v for v in out.values() if not v.get("error")]
    print(f"\n{len(ok)}/{len(out)} portals, "
          f"{sum(len(v['datasets']) for v in ok):,} datasets -> {OUT}")


if __name__ == "__main__":
    main()
