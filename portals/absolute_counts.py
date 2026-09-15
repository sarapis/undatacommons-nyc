#!/usr/bin/env python3
"""Count, per municipal portal, how many UN indicators clear a FIXED similarity bar.

The percentile cutoff used for per-city worksheets keeps the top ~20% by design,
so it is top-coded: 28 portals scored exactly 12 and were indistinguishable. That
is the right behaviour for bounding one city's review list and useless as a
comparative column.

These counts use absolute bars instead. Scores are not perfectly comparable
across catalogs -- that is why the worksheet cutoff is calibrated -- but a fixed
bar at least varies with the data rather than with the parameter.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "probe"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import embed, scope                          # noqa: E402
from portal import Portal                    # noqa: E402
from matchable import language_for           # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
INV = ROOT / "portals" / "inventory.json"
BARS = (0.45, 0.50, 0.55, 0.60)

inv = json.loads(INV.read_text())
muni = [r for r in inv["rows"] if r.get("candidates") is not None]
ind = [r for r in json.loads((ROOT / "probe/cache/screened.json").read_text())["indicators"]
       if r.get("grade") in ("GREEN", "AMBER", "RANK-ONLY")]
ind.sort(key=lambda r: -(r.get("panel_coverage") or 0))
sc = scope.Scoper()
ind = [r for r in ind if sc.is_city(r.get("name"), scope.THRESHOLD)][:60]
print(f"{len(muni)} portals x {len(ind)} indicators", file=sys.stderr)

for i, r in enumerate(muni, 1):
    host = r["portal"]
    key = "inv-" + host.replace(".", "-")
    try:
        city = {"key": key, "name": host, "platform": r["platform"],
                "domain": host if r["platform"] == "socrata" else r["url"]}
        cat = Portal(city).catalog(limit=1500)
        idx = embed.Index(datasets=cat, cache_key=key,
                          language=r.get("match_language", language_for(host)))
        tops = [idx.search(x.get("name") or "", k=1)[0]["score"] for x in ind]
        for b in BARS:
            r[f"above_{b}"] = sum(1 for t in tops if t >= b)
        r["best"] = round(max(tops), 3)
        print(f"  [{i}/{len(muni)}] {host:<34} best {r['best']:.2f} "
              f"| >=.50 {r['above_0.5']:>2} | >=.55 {r['above_0.55']:>2}", file=sys.stderr)
    except Exception as exc:                                 # noqa: BLE001
        r["abs_error"] = type(exc).__name__
        print(f"  [{i}/{len(muni)}] {host:<34} FAILED {type(exc).__name__}", file=sys.stderr)
    if i % 10 == 0:                     # checkpoint, so a crash does not lose everything
        INV.write_text(json.dumps(inv, indent=1))

INV.write_text(json.dumps(inv, indent=1))
done = sum(1 for r in muni if "above_0.5" in r)
print(f"\ncomputed {done} of {len(muni)}", file=sys.stderr)
