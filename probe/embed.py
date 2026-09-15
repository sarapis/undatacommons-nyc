"""Embedding search over the NYC Open Data catalog.

Replaces keyword overlap, which was measurably terrible: against seven pairs we
had already verified by hand, keyword scoring put the correct dataset at a
median rank of 1535 out of 2400. Embeddings put it at 23.

Uses model2vec static embeddings -- CPU-only, no torch, a few tens of MB. If it
is not installed the pipeline falls back to keyword matching and says so loudly,
so the repo keeps its "clone and run" property for collaborators.

    pip3 install model2vec

Measured on the verified pairs (2,400 datasets, potion-base-32M):

    keyword overlap          median rank 1535   top-50  2/7
    embeddings title+desc    median rank   27   top-50  4/7
    embeddings enriched      median rank   23   top-50  5/7

Two of the seven stay unfindable at any rank, and the reason matters: the NYC
homicide series lives inside "NYPD Complaint Data Historic" as offence code 101,
a fact present nowhere in that dataset's metadata. No text method can recover a
mapping that depends on knowing what is *inside* a dataset. The shortlist is a
triage aid for a human, not a discovery engine.
"""

import json
import pathlib
import sys

CACHE = pathlib.Path(__file__).resolve().parent / "cache"
CATALOG = CACHE / "nyc_catalog.json"
VECTORS = CACHE / "nyc_catalog_vectors.npz"
# Two models, chosen by the catalog's language -- not one model for everything.
#
# Measured on the seven hand-verified NYC pairs (2,400 datasets), the English
# model puts the correct dataset at median rank 23 and the multilingual one at
# 81, so swapping wholesale would have cost real accuracy on English catalogs.
# But the English model scores Madrid at 0.27 and Milan at 0.29 -- noise -- so
# non-English catalogs get nothing from it at all. Hence: pick per language.
MODEL = "minishlab/potion-base-32M"
MODEL_MULTILINGUAL = "minishlab/potion-multilingual-128M"


def model_for(language):
    return MODEL if (language or "en").lower().startswith("en") else MODEL_MULTILINGUAL


def available():
    try:
        import model2vec  # noqa: F401
        import numpy  # noqa: F401
        return True
    except ImportError:
        return False


def dataset_text(d):
    """Text to embed. Columns, tags and category carry real signal.

    Adding them moved 'Proportion of municipal waste recycled' -> DSNY Monthly
    Tonnage from rank 882 to 23, because the title never says "recycled".
    """
    parts = [d.get("name", ""), d.get("category", ""), " ".join(d.get("tags", []) or []),
             d.get("description", "")]
    cols = d.get("columns") or []
    if cols:
        parts.append("Fields: " + ", ".join(cols[:25]))
    parts.append(" ".join((d.get("column_descriptions") or [])[:15]))
    # CKAN portals almost never publish field names, so this degrades to
    # title + description + tags there. That is a real coverage asymmetry
    # between platforms, not a bug.
    return ". ".join(p for p in parts if p)


class Index:
    """Embedding index over one city's catalog.

    `datasets` may be passed directly (any city, via probe/portal.py) or left
    None to load the cached NYC catalog, which is how the original NYC-only
    pipeline calls it.
    """

    def __init__(self, datasets=None, cache_key="nyc", language="en"):
        import numpy as np
        from model2vec import StaticModel
        self.np = np
        self.datasets = (datasets if datasets is not None
                         else json.loads(CATALOG.read_text())["datasets"])
        self.model_name = model_for(language)
        self.model = StaticModel.from_pretrained(self.model_name)
        # The model is part of the cache identity: vectors from two different
        # models are not interchangeable and must never be reused across them.
        tag = "" if self.model_name == MODEL else "-ml"
        vec_path = (VECTORS if (cache_key == "nyc" and not tag)
                    else CACHE / f"{cache_key}{tag}_catalog_vectors.npz")
        if vec_path.exists():
            cached = np.load(vec_path, allow_pickle=True)
            if len(cached["ids"]) == len(self.datasets):
                self.vectors = cached["vectors"]
                return
        print(f"  embedding {len(self.datasets)} datasets ({cache_key}, "
              f"{self.model_name.split('/')[-1]})...", file=sys.stderr)
        vecs = self.model.encode([dataset_text(d) for d in self.datasets],
                                 show_progress_bar=False)
        self.vectors = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
        vec_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(vec_path, vectors=self.vectors,
                            ids=np.array([d["id"] for d in self.datasets]))

    def search(self, query, k=5):
        """Top-k matches, each carrying a z-score as well as a raw similarity.

        The raw cosine cannot be thresholded across catalogs -- measured on the
        hand-judged set in probe/match_eval.json, the good matches span 0.42-0.70
        in NYC but 0.37-0.59 in Madrid and 0.50-0.55 in Chicago, so one cutoff is
        simultaneously too strict and too loose. The z-score asks how far the
        match stands above *this* catalog's own distribution for *this* query,
        which does travel.
        """
        v = self.model.encode([query], show_progress_bar=False)[0]
        v = v / self.np.linalg.norm(v)
        sims = self.vectors @ v
        mean, std = float(sims.mean()), float(sims.std()) or 1e-9
        out = []
        for i in self.np.argsort(-sims)[:k]:
            d = dict(self.datasets[int(i)])
            s = float(sims[int(i)])
            d["score"] = round(s, 3)
            d["z"] = round((s - mean) / std, 2)
            out.append(d)
        return out
