#!/usr/bin/env python3
"""Categories cities publish that the SDG framework has no words for.

The inverse crosswalk clusters the far tail of every municipal catalog and reads
the themes off it. Clustering is a weak instrument -- k-means returns k clusters
whether or not k themes exist, and its city counts move when k moves. This
measures the same categories a second way, without clustering at all:

  1. search every NAMED SDG indicator for the category's vocabulary, and
  2. count the municipal datasets whose titles carry it, by city.

Both halves are greppable and neither depends on an embedding. That matters
because the cluster count and the vocabulary count disagree: the FOIA cluster
spanned 15 cities, and only 8 of them publish a dataset that actually says so --
cluster membership swept in "Media Releases" and "City Hall Library Catalog",
which are not request logs. The vocabulary count is the defensible one.

The embedding is still used for one thing: how far each of these datasets sits
from the framework, which is the claim being made about them.

Usage:  python3 probe/category_gaps.py
Writes docs/artifacts/category-gaps-<date>.json.
"""

import collections
import datetime as dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "probe"))
import embed                                   # noqa: E402

CACHE = ROOT / "probe" / "cache"
ARTIFACTS = ROOT / "docs" / "artifacts"
TAIL_FRACTION = 0.25

CATEGORIES = {
    "elections": {
        "label": "Electoral administration",
        # Six languages, because the category has to be counted in the languages
        # the cities publish in or it is only a finding about anglophone cities.
        "municipal": r"\belecci|\belezion|\belection|\bwahl|\belei[çc][ãa]o|\beleitor|"
                     r"\bvoting\b|\bvoter\b|\bballot|referend|\belectoral|mesas electorales|"
                     r"\bpolling\b|poll site|\bprecinct|partidos pol[íi]ticos",
        "framework": r"\belection|\belectoral|\bvot(e|er|ing|es)\b|turnout|ballot|referend|"
                     r"suffrag|polling|candidat",
    },
    "records access": {
        "label": "Records-access requests",
        "municipal": r"\bfoia\b|freedom of information|public records request|\brecords request|"
                     r"information request|open records|acesso [àa] informa|transpar[êe]ncia|"
                     r"transparencia|solicitud(es)? de informaci|informationsfreiheit",
        "framework": r"access to information|right to information|freedom of information",
    },
}


def main():
    import numpy as np
    from model2vec import StaticModel

    cats = json.loads((CACHE / "municipal-catalogs.json").read_text())
    names = {r["dcid"]: r.get("name") for r in
             json.loads((CACHE / "screened.json").read_text())["indicators"] if r.get("name")}
    bases = json.loads((CACHE / "corpus.json").read_text())["bases"]
    inds = [(d, names[d]) for d in sorted(bases) if d in names]

    rows = []
    for group, model_lang in (("en", "en"), ("non-en", "es")):
        ps = [v for v in cats.values() if not v.get("error")
              and len(v.get("datasets") or []) >= 25
              and ((v.get("language") == "en") if group == "en"
                   else (v.get("language") != "en"))]
        model = StaticModel.from_pretrained(embed.model_for(model_lang))
        I = model.encode([n for _, n in inds], show_progress_bar=False)
        I = I / np.linalg.norm(I, axis=1, keepdims=True)
        for p in ps:
            ds = p["datasets"]
            idx = embed.Index(ds, cache_key=p["key"], language=model_lang)
            sims = np.maximum(idx.head @ I.T, idx.body @ I.T)
            aff, best = sims.max(axis=1), sims.argmax(axis=1)
            cut = np.sort(aff)[max(int(len(aff) * TAIL_FRACTION) - 1, 0)]
            for i, d in enumerate(ds):
                rows.append({"city": p.get("city") or p["portal"],
                             "name": d.get("name") or "", "affinity": float(aff[i]),
                             "in_tail": bool(aff[i] <= cut),
                             "nearest": inds[int(best[i])][1]})

    overall = sum(r["affinity"] for r in rows) / len(rows)
    out = {"generated": dt.date.today().isoformat(),
           "datasets_scanned": len(rows), "cities": len({r["city"] for r in rows}),
           "named_indicators": len(inds), "mean_affinity_all": round(overall, 3),
           "categories": {}}

    for key, spec in CATEGORIES.items():
        mpat, fpat = re.compile(spec["municipal"], re.I), re.compile(spec["framework"], re.I)
        fw = [{"dcid": d, "name": n} for d, n in inds if fpat.search(n)]
        hit = [r for r in rows if mpat.search(r["name"])]
        by_city = collections.Counter(r["city"] for r in hit)
        out["categories"][key] = {
            "label": spec["label"],
            "framework_indicators": fw,
            "n_framework": len(fw),
            "n_datasets": len(hit), "n_cities": len(by_city),
            "in_tail": sum(1 for r in hit if r["in_tail"]),
            "mean_affinity": round(sum(r["affinity"] for r in hit) / max(len(hit), 1), 3),
            "top_city": by_city.most_common(1)[0] if by_city else None,
            "by_city": by_city.most_common(),
            "nearest_offered": collections.Counter(r["nearest"] for r in hit).most_common(5),
            "examples": [f"{r['name']} — {r['city']}" for r in hit[:10]],
        }

    today = out["generated"]
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / f"category-gaps-{today}.json").write_text(json.dumps(out, indent=1))
    print(f"scanned {len(rows):,} datasets across {out['cities']} cities")
    for key, c in out["categories"].items():
        dom = c["top_city"]
        print(f"\n{c['label']}")
        print(f"  framework: {c['n_framework']} of {len(inds)} named indicators")
        print(f"  municipal: {c['n_datasets']} datasets across {c['n_cities']} cities "
              f"({c['in_tail']} in tail), mean affinity {c['mean_affinity']} vs {overall:.3f}")
        if dom:
            print(f"  most concentrated: {dom[0]} with {dom[1]} "
                  f"({100 * dom[1] // c['n_datasets']}% of the category)")
    print(f"\nwrote docs/artifacts/category-gaps-{today}.json")


if __name__ == "__main__":
    main()
