#!/usr/bin/env python3
"""Fetch and cache the full NYC Open Data catalog.

The keyword matcher could only ever rank what Socrata's own keyword search
returned, which made retrieval -- not scoring -- the real ceiling. Holding the
whole catalog locally removes that: every indicator is compared against every
dataset.

Usage:  python3 probe/catalog.py
Writes probe/cache/nyc_catalog.json (~2,400 datasets).
"""

import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nyc  # noqa: E402

CACHE = pathlib.Path(__file__).resolve().parent / "cache"
OUT = CACHE / "nyc_catalog.json"
PAGE = 100


def fetch_all():
    rows, offset = [], 0
    while True:
        d = nyc._get(nyc.CATALOG, {"domains": nyc.DOMAIN, "only": "dataset",
                                   "limit": PAGE, "offset": offset})
        results = d.get("results") or []
        if not results:
            break
        for r in results:
            res = r.get("resource", {})
            cls = r.get("classification", {}) or {}
            # Column names, descriptions, category and tags matter more than they
            # look. A dataset called "NYPD Complaint Data Historic" never says
            # "homicide" in its title -- the concept lives in its columns and in
            # tags like "crime". Title-only retrieval cannot find it at all.
            rows.append({
                "id": res.get("id"),
                "name": res.get("name") or "",
                "description": (res.get("description") or "")[:1500],
                "columns": (res.get("columns_name") or [])[:40],
                "column_descriptions": [c for c in (res.get("columns_description") or [])[:40] if c],
                "category": cls.get("domain_category") or "",
                "tags": (cls.get("domain_tags") or [])[:12],
                "updated": (res.get("updatedAt") or "")[:10],
                "archived": (res.get("name") or "").upper().startswith("ARCHIVED"),
            })
        offset += PAGE
        print(f"  {len(rows)} / {d.get('resultSetSize')}", file=sys.stderr)
        if offset >= (d.get("resultSetSize") or 0):
            break
        time.sleep(0.2)
    return rows


if __name__ == "__main__":
    CACHE.mkdir(parents=True, exist_ok=True)
    rows = fetch_all()
    OUT.write_text(json.dumps({"count": len(rows), "datasets": rows}, indent=1))
    print(f"\nwrote {OUT} ({len(rows)} datasets)")
