#!/usr/bin/env python3
"""The inverse crosswalk — municipal data the SDG framework has no words for.

Everything else in this repo runs city -> UN: take an SDG indicator, find the
municipal dataset that matches it. That direction can only ever discover what
the framework already asks about. This runs it backwards. Take every dataset a
city publishes, find its nearest SDG indicator, and look at what is left over.

The question is not "which cities are behind" -- it is **what would SDG 11 look
like if it had been written from municipal data upward?**

WHAT THE RESULT MEANS, PRECISELY. A dataset far from every indicator means no
SDG indicator's *text* is near this dataset's *text*. That is evidence of a gap
in the framework's vocabulary, and it is NOT the same thing as a conceptual gap:
this repo has already learned once that a null from the matcher is not evidence
of absence (Boston's Vision Zero file ranked 23rd for road deaths, below a
contract-award file). Three defences, none sufficient alone:

  1. Positive controls. Datasets from the hand-verified crosswalk must land in
     the HIGH-affinity region. If a known match lands in the tail, the signal is
     noise and the run says so instead of reporting themes.
  2. Aggregation. One dataset scoring low is retrieval failure. Four hundred
     datasets about parking permits scoring low is a pattern.
  3. Cities, not datasets, are the unit of evidence. A theme that appears in
     thirty independent city catalogs is a category of municipal governance. A
     theme in one is that city's filing habit.

Scope note: matched against all 689 enumerated SDG indicators, not the 442 with
usable data. A framework gap is a question about vocabulary, not coverage.

Usage:  python3 probe/inverse.py [--clusters 24] [--language en]
Reads probe/cache/municipal-catalogs.json (make it with probe/fetch_municipal.py).
Writes docs/artifacts/inverse-<date>.{json,md}.
"""

import argparse
import collections
import datetime as dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "probe"))
import embed                                      # noqa: E402

CACHE = ROOT / "probe" / "cache"
CATALOGS = CACHE / "municipal-catalogs.json"
CORPUS = CACHE / "corpus.json"
SCREENED = CACHE / "screened.json"
ARTIFACTS = ROOT / "docs" / "artifacts"

# The tail is selected per catalog, never with one absolute bar. Good matches
# span 0.42-0.70 in NYC and 0.37-0.59 in Madrid, so a fixed cutoff is at once
# too strict and too loose -- established the expensive way, see decisions.md.
# A percentile keeps a fixed FRACTION by construction, which makes it useless
# for ranking cities against each other and exactly right for what it is used
# for here: bounding a pool within each catalog on comparable terms.
TAIL_FRACTION = 0.25

# Mean cosine of a cluster's members to its own centroid. Below this, k-means has
# returned a partition rather than a theme, and the cluster is published as
# diffuse instead of being read as a finding. Set by reading the clusters.
COHERENCE_FLOOR = 0.62

STOP = set("""a an the of and or for in on at to by with from data dataset datasets set
list report reports city county state department dept annual monthly yearly quarterly
daily weekly current historical history archive archived public open new all total
number count summary detail details info information service services program programs
2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 fy""".split())


def indicator_texts():
    """All 689 enumerated base indicators, with the best name we have for each."""
    names = {r["dcid"]: r.get("name") for r in
             json.loads(SCREENED.read_text())["indicators"] if r.get("name")}
    bases = json.loads(CORPUS.read_text())["bases"]
    out = []
    for dcid in sorted(bases):
        name = names.get(dcid)
        if not name:
            # No screened name: fall back to the DCID's own mnemonic, which is
            # poor query text. Counted and reported rather than hidden.
            name = dcid.rsplit("/", 1)[-1].replace("_", " ")
            out.append((dcid, name, False))
        else:
            out.append((dcid, name, True))
    return out


def tokens(text):
    return [w for w in re.findall(r"[a-z][a-z'-]{2,}", (text or "").lower())
            if w not in STOP]


def kmeans(np, X, k, iters=40, seed=0):
    """Spherical k-means. Vectors are unit-norm, so centroids are renormalised."""
    rng = np.random.default_rng(seed)
    # k-means++ style seeding, cheap version: first centre random, rest far away.
    idx = [int(rng.integers(len(X)))]
    d = 1.0 - X @ X[idx[0]]
    for _ in range(k - 1):
        p = np.maximum(d, 0) ** 2
        tot = float(p.sum())
        idx.append(int(rng.choice(len(X), p=p / tot)) if tot > 0
                   else int(rng.integers(len(X))))
        d = np.minimum(d, 1.0 - X @ X[idx[-1]])
    C = X[idx].copy()
    labels = np.zeros(len(X), dtype=int)
    for _ in range(iters):
        sims = X @ C.T
        new = sims.argmax(axis=1)
        if (new == labels).all():
            break
        labels = new
        for j in range(k):
            m = labels == j
            if m.any():
                c = X[m].mean(axis=0)
                n = np.linalg.norm(c)
                C[j] = c / n if n else C[j]
    return labels, C


def _spread_examples(members, n=8):
    seen, out, rest = set(), [], []
    for m in members:
        city = m["city"] or m["portal"]
        (out if city not in seen else rest).append(m)
        seen.add(city)
    return [f"{m['name']} — {m['city'] or m['portal']}" for m in (out + rest)[:n]]


def label_cluster(titles, corpus_df, n_corpus, top=7):
    """Terms that are distinctive of this cluster, not merely frequent in it."""
    df = collections.Counter()
    for t in titles:
        df.update(set(tokens(t)))
    scored = []
    for term, c in df.items():
        coverage = c / len(titles)
        # Lift alone picks rare terms that a handful of members happen to share:
        # a 144-member cluster was labelled "inch, sea, rise" off a few coastal
        # datasets, and the label described almost none of it. Require the term
        # to cover a fifth of the cluster before its distinctiveness counts.
        if c < 3 or coverage < 0.20:
            continue
        lift = coverage / max(corpus_df.get(term, 1) / n_corpus, 1e-9)
        scored.append((coverage * lift, c, term))
    scored.sort(reverse=True)
    return [t for _, _, t in scored[:top]] or ["(no term covers a fifth of this cluster)"]


def phrase_themes(rows, min_cities=4, top=40):
    """Frequent title phrases in the tail, counted by DISTINCT CITIES.

    k-means over static embeddings of short titles is a weak instrument -- it
    returns k clusters whether or not k themes exist, and on the first run about
    half of them were mush. Bigrams from the titles themselves are cruder and
    far more legible: "street sweeping", "building permit", "foia request" are
    not inferred, they are literally what the cities called the data.

    Counted by city, never by dataset. One city publishing forty parking files
    is a filing habit; twenty cities each publishing one is a category of
    municipal governance that the SDG framework has no words for.
    """
    tail = [r for r in rows if r["in_tail"]]
    by_phrase = collections.defaultdict(lambda: {"cities": set(), "n": 0, "examples": []})
    for r in tail:
        t = tokens(r["name"])
        city = r["city"] or r["portal"]
        for a, b in zip(t, t[1:]):
            e = by_phrase[f"{a} {b}"]
            e["cities"].add(city)
            e["n"] += 1
            if len(e["examples"]) < 6 and all(x[1] != city for x in e["examples"]):
                e["examples"].append((r["name"], city))
    out = [{"phrase": p, "n_cities": len(v["cities"]), "n": v["n"],
            "examples": [f"{n} — {c}" for n, c in v["examples"]]}
           for p, v in by_phrase.items() if len(v["cities"]) >= min_cities]
    out.sort(key=lambda e: (-e["n_cities"], -e["n"]))
    return out[:top]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clusters", type=int, default=24)
    ap.add_argument("--language", default="en")
    ap.add_argument("--min-datasets", type=int, default=25,
                    help="skip portals smaller than this; they cannot support a tail")
    args = ap.parse_args()

    import numpy as np
    from model2vec import StaticModel

    cats = json.loads(CATALOGS.read_text())
    portals = [v for v in cats.values()
               if not v.get("error") and v.get("language") == args.language
               and len(v.get("datasets") or []) >= args.min_datasets]
    portals.sort(key=lambda v: -len(v["datasets"]))
    print(f"{len(portals)} portals in language '{args.language}', "
          f"{sum(len(p['datasets']) for p in portals):,} datasets", file=sys.stderr)

    inds = indicator_texts()
    named = sum(1 for _, _, ok in inds if ok)
    model = StaticModel.from_pretrained(embed.model_for(args.language))
    I = model.encode([n for _, n, _ in inds], show_progress_bar=False)
    I = I / np.linalg.norm(I, axis=1, keepdims=True)
    print(f"{len(inds)} SDG indicators embedded ({named} with a real name)", file=sys.stderr)

    rows, heads = [], []
    for p in portals:
        ds = p["datasets"]
        idx = embed.Index(ds, cache_key=p.get("key") or ("inv-" + p["portal"].replace(".", "-")),
                          language=args.language)
        sims = np.maximum(idx.head @ I.T, idx.body @ I.T)      # (n_datasets, n_indicators)
        best = sims.argmax(axis=1)
        aff = sims.max(axis=1)
        order = np.argsort(aff)
        cut = aff[order[max(int(len(aff) * TAIL_FRACTION) - 1, 0)]]
        for i, d in enumerate(ds):
            rows.append({"portal": p["portal"], "city": p.get("city"),
                         "id": d.get("id"), "name": d.get("name") or "",
                         "affinity": float(aff[i]),
                         "nearest_dcid": inds[int(best[i])][0],
                         "nearest_name": inds[int(best[i])][1],
                         "in_tail": bool(aff[i] <= cut)})
        heads.append(idx.head)
        print(f"  {p['portal']:<40}{len(ds):>5} datasets  "
              f"affinity med {float(np.median(aff)):.3f}  tail<= {float(cut):.3f}",
              file=sys.stderr)
    H = np.vstack(heads)

    # --- positive controls -------------------------------------------------
    cw = json.loads((ROOT / "probe" / "crosswalk.json").read_text())["pairs"]
    want = {p["nyc"]["dataset"]: p["label"] for p in cw if p.get("nyc")}
    by_id = {r["id"]: r for r in rows if r["portal"] == "data.cityofnewyork.us"}
    nyc_aff = sorted(r["affinity"] for r in rows if r["portal"] == "data.cityofnewyork.us")
    controls = []
    for did, label in want.items():
        r = by_id.get(did)
        if not r:
            controls.append({"dataset": did, "label": label, "found": False})
            continue
        pct = 100.0 * sum(1 for a in nyc_aff if a < r["affinity"]) / max(len(nyc_aff), 1)
        controls.append({"dataset": did, "label": label, "found": True,
                         "name": r["name"], "affinity": round(r["affinity"], 3),
                         "percentile": round(pct, 1), "in_tail": r["in_tail"],
                         "nearest": r["nearest_name"]})
    ok_controls = [c for c in controls if c.get("found")]
    in_tail = [c for c in ok_controls if c["in_tail"]]

    # --- cluster the tail --------------------------------------------------
    tail_i = [i for i, r in enumerate(rows) if r["in_tail"]]
    Xt = H[tail_i]
    labels, C = kmeans(np, Xt, args.clusters)
    corpus_df = collections.Counter()
    for r in rows:
        corpus_df.update(set(tokens(r["name"])))

    clusters = []
    for j in range(args.clusters):
        sel = [k for k in range(len(tail_i)) if labels[k] == j]
        members = [rows[tail_i[k]] for k in sel]
        if not members:
            continue
        # How tight is this cluster actually? Mean cosine of its members to its
        # own centroid. k-means always returns k clusters; it does not promise
        # any of them mean anything, and half of the first run's did not.
        coherence = float((Xt[sel] @ C[j]).mean())
        titles = [m["name"] for m in members]
        cities = {m["city"] or m["portal"] for m in members}
        near = collections.Counter(m["nearest_name"] for m in members)
        clusters.append({
            "terms": label_cluster(titles, corpus_df, len(rows)),
            "n": len(members), "n_cities": len(cities),
            "cities": sorted(c for c in cities if c)[:10],
            "mean_affinity": round(sum(m["affinity"] for m in members) / len(members), 3),
            "coherence": round(coherence, 3),
            "diffuse": bool(coherence < COHERENCE_FLOOR),
            # One example per city before a second from any city: taking the
            # first N returns eight NYC rows, because NYC is the largest catalog
            # and therefore first in row order.
            "examples": _spread_examples(members),
            "nearest_indicator_most_common": near.most_common(1)[0][0] if near else None,
        })
    clusters.sort(key=lambda c: (-c["coherence"], -c["n_cities"]))
    phrases = phrase_themes(rows)

    # --- the column view: indicators nothing comes near ---------------------
    best_for_ind = {}
    for r in rows:
        d = r["nearest_dcid"]
        if r["affinity"] > best_for_ind.get(d, -1):
            best_for_ind[d] = r["affinity"]
    never = [(d, n) for d, n, _ in inds if d not in best_for_ind]

    today = dt.date.today().isoformat()
    out = {"generated": today, "language": args.language,
           "portals": len(portals), "datasets": len(rows), "indicators": len(inds),
           "indicators_with_real_name": named,
           "tail_fraction": TAIL_FRACTION, "tail_size": len(tail_i),
           "controls": controls, "clusters": clusters, "phrases": phrases,
           "coherence_floor": COHERENCE_FLOOR,
           "indicators_never_nearest": [{"dcid": d, "name": n} for d, n in never]}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / f"inverse-{today}.json").write_text(json.dumps(out, indent=1))
    (ARTIFACTS / f"inverse-{today}.md").write_text(render(out))
    (ARTIFACTS / "inverse-latest.md").write_text(render(out))

    print(f"\npositive controls: {len(ok_controls)} found, {len(in_tail)} fell in the tail")
    for c in ok_controls:
        print(f"   {'TAIL' if c['in_tail'] else 'ok  '} p{c['percentile']:>5.1f}  "
              f"{c['label'][:38]:<40}{c['name'][:44]}")
    print(f"\n{len(clusters)} clusters over {len(tail_i):,} tail datasets")
    print(f"{'cities':>7}{'n':>7}  terms")
    for c in clusters[:20]:
        print(f"{c['n_cities']:>7}{c['n']:>7}  {', '.join(c['terms'][:6])}")
    print(f"\n{len(never)} of {len(inds)} indicators were nearest to no dataset at all")
    print(f"wrote docs/artifacts/inverse-{today}.md")


def render(o):
    md = ["---", "layout: default", f"title: Inverse crosswalk — {o['generated']}", "---", "",
          f"# The inverse crosswalk — {o['generated']}", "",
          "Every other analysis here runs city → UN: take an SDG indicator, find the "
          "municipal dataset that matches it. That can only discover what the framework "
          "already asks about. This runs it backwards — take every dataset a city "
          "publishes, find its nearest SDG indicator, and look at what is left over.", "",
          f"**{o['datasets']:,} datasets** from **{o['portals']} city portals** "
          f"(language `{o['language']}`), matched against **all {o['indicators']} enumerated "
          f"SDG indicators** — not the 442 with usable data, because a framework gap is a "
          f"question about vocabulary rather than coverage.", "",
          "**What a result here means.** A dataset far from every indicator means no SDG "
          "indicator's *text* is near this dataset's *text*. That is evidence about "
          "vocabulary, not proof of a conceptual gap — this project has already learned "
          "once that a null from the matcher is not evidence of absence. So the unit of "
          "evidence below is **how many independent cities** a theme appears in. A theme "
          "in thirty city catalogs is a category of municipal governance; a theme in one "
          "is that city's filing habit.", ""]

    ok = [c for c in o["controls"] if c.get("found")]
    bad = [c for c in ok if c["in_tail"]]
    md += ["## Positive controls", "",
           "Datasets from the hand-verified NYC crosswalk. These are known to correspond to "
           "an SDG indicator, so they must land in the high-affinity region. If they fall "
           "in the tail, the tail is measuring retrieval failure and nothing below is "
           "trustworthy.", "",
           f"**{len(ok)} of {len(o['controls'])} located · {len(bad)} fell in the tail.**", "",
           "| Verified pair | NYC dataset | Affinity | Percentile | In tail? |",
           "|---|---|---:|---:|---|"]
    for c in sorted(ok, key=lambda c: -c["percentile"]):
        md.append(f"| {c['label']} | {c['name'][:44]} | {c['affinity']} | "
                  f"{c['percentile']:.0f} | {'**YES**' if c['in_tail'] else 'no'} |")

    md += ["", "## What cities publish that the SDGs have no words for", "",
           f"The bottom **{o['tail_fraction']:.0%} of each catalog** by affinity — "
           f"{o['tail_size']:,} datasets. Below are the title phrases that recur across "
           "that tail, **counted by how many independent cities use them**. These are not "
           "inferred categories; they are what the cities themselves called the data.", "",
           "| Cities | Datasets | Phrase |", "|---:|---:|---|"]
    for e in o.get("phrases", []):
        md.append(f"| {e['n_cities']} | {e['n']} | **{e['phrase']}** |")

    md += ["", "### In detail", ""]
    for e in o.get("phrases", [])[:14]:
        md += [f"**{e['phrase']}** — {e['n']} datasets across {e['n_cities']} cities", "",
               "".join(f"- {t}\n" for t in e["examples"][:5]), ""]

    solid = [c for c in o["clusters"] if not c["diffuse"]]
    diffuse = [c for c in o["clusters"] if c["diffuse"]]
    md += ["", "## The same tail, clustered by embedding", "",
           "A second view, kept because it groups datasets that share no vocabulary. "
           "k-means returns *k* clusters whether or not *k* themes exist, so each carries "
           "its **coherence** — the mean cosine of its members to its own centroid. "
           f"Below {o['coherence_floor']}, a cluster is a partition rather than a theme and "
           f"is marked diffuse; **{len(diffuse)} of {len(o['clusters'])} are.** Read those "
           "as noise, not as findings.", "",
           "| Coherence | Cities | Datasets | Terms | Closest SDG indicator |",
           "|---:|---:|---:|---|---|"]
    for c in o["clusters"]:
        mark = " *(diffuse)*" if c["diffuse"] else ""
        md.append(f"| {c['coherence']}{mark} | {c['n_cities']} | {c['n']} | "
                  f"{', '.join(c['terms'][:5])} | "
                  f"{(c['nearest_indicator_most_common'] or '—')[:44]} |")

    md += ["", "### The coherent clusters in detail", ""]
    for c in solid[:10]:
        md += [f"**{', '.join(c['terms'][:5])}** — {c['n']} datasets across "
               f"{c['n_cities']} cities (coherence {c['coherence']}, "
               f"mean affinity {c['mean_affinity']})", "",
               "".join(f"- {t}\n" for t in c["examples"][:5]), ""]

    md += ["", "## Reproducing", "", "```bash",
           "python3 probe/fetch_municipal.py", "python3 probe/inverse.py", "```", ""]
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    main()
