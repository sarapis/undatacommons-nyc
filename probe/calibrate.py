#!/usr/bin/env python3
"""Compare ways of deciding whether a match is worth showing.

An absolute cosine cutoff was calibrated on NYC's 2,400-dataset catalog and does
not survive contact with any other catalog: in a smaller or differently-worded
corpus the nearest neighbour is simply whatever is least unrelated, and 0.50
starts admitting drinking fountains for pets.

The alternatives here all ask a *relative* question instead:

  zscore  how far above this catalog's own similarity distribution the top match
          sits, for this query -- (top - mean) / std over all datasets
  margin  how far the top match sits above the runner-up; a distinctive match
          beats its neighbours, a generic one does not
  both    require the match to clear a floor on each

Scored against probe/match_eval.json, which is hand-judged and contestable.

    python3 probe/calibrate.py
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import embed                       # noqa: E402
from portal import Portal          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVAL = ROOT / "probe" / "match_eval.json"
REGISTRY = ROOT / "cities" / "registry.json"


def stats_for(index, query):
    """Top similarity, plus how unusual it is within this catalog."""
    np = index.np
    v = index.model.encode([query], show_progress_bar=False)[0]
    v = v / np.linalg.norm(v)
    sims = index.vectors @ v
    order = np.argsort(-sims)
    top = float(sims[order[0]])
    second = float(sims[order[1]]) if len(order) > 1 else 0.0
    mean, std = float(sims.mean()), float(sims.std()) or 1e-9
    return {"top": top, "z": (top - mean) / std, "margin": top - second,
            "dataset": index.datasets[int(order[0])]["id"]}


def main():
    cases = json.loads(EVAL.read_text())["cases"]
    cities = {c["key"]: c for c in json.loads(REGISTRY.read_text())["cities"]}

    by_city = {}
    for c in cases:
        by_city.setdefault(c["city"], []).append(c)

    scored = []
    for key, group in by_city.items():
        city = cities[key]
        if key == "nyc":
            datasets = json.loads((ROOT / "probe" / "cache" / "nyc_catalog.json").read_text())["datasets"]
        else:
            datasets = Portal(city).catalog(limit=3000)
        index = embed.Index(datasets=datasets, cache_key=key,
                            language=city.get("language", "en"))
        for c in group:
            s = stats_for(index, c["indicator"])
            s["good"] = c["good"]
            s["city"] = key
            scored.append(s)
        print(f"  {city['name']:<14} {len(group)} cases", file=sys.stderr)

    def report(label, fn):
        tp = sum(1 for s in scored if s["good"] and fn(s))
        fp = sum(1 for s in scored if not s["good"] and fn(s))
        fn_ = sum(1 for s in scored if s["good"] and not fn(s))
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn_) if tp + fn_ else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        print(f"  {label:<26} precision {prec:.2f}  recall {rec:.2f}  F1 {f1:.2f}"
              f"   (tp {tp} fp {fp} fn {fn_})")
        return f1

    print(f"\n{len(scored)} cases, {sum(1 for s in scored if s['good'])} good\n")
    print("  absolute cutoff (the current approach, calibrated on NYC):")
    for t in (0.45, 0.50, 0.55):
        report(f"top >= {t}", lambda s, t=t: s["top"] >= t)
    print("\n  relative to this catalog's own distribution:")
    for z in (2.5, 3.0, 3.5, 4.0):
        report(f"z >= {z}", lambda s, z=z: s["z"] >= z)
    print("\n  distinctiveness over the runner-up:")
    for mg in (0.01, 0.02, 0.03):
        report(f"margin >= {mg}", lambda s, mg=mg: s["margin"] >= mg)
    print("\n  combined:")
    best, bestf1 = None, -1
    for z in (2.5, 3.0, 3.5):
        for mg in (0.0, 0.01, 0.02):
            f1 = report(f"z >= {z} and margin >= {mg}",
                        lambda s, z=z, mg=mg: s["z"] >= z and s["margin"] >= mg)
            if f1 > bestf1:
                best, bestf1 = (z, mg), f1
    print(f"\n  best combined: z >= {best[0]}, margin >= {best[1]}  (F1 {bestf1:.2f})")

    print("\n  per-city top-score ranges (why an absolute cutoff cannot travel):")
    for key in by_city:
        xs = [s["top"] for s in scored if s["city"] == key]
        zs = [s["z"] for s in scored if s["city"] == key]
        print(f"    {key:<9} top {min(xs):.2f}–{max(xs):.2f}   z {min(zs):.1f}–{max(zs):.1f}")


if __name__ == "__main__":
    main()
