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
MODEL = "minishlab/potion-base-32M"


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
    return (f"{d['name']}. {d.get('category','')}. {' '.join(d.get('tags', []))}. "
            f"{d.get('description','')} "
            f"Fields: {', '.join(d.get('columns', [])[:25])}. "
            f"{' '.join(d.get('column_descriptions', [])[:15])}")


class Index:
    def __init__(self):
        import numpy as np
        from model2vec import StaticModel
        self.np = np
        self.datasets = json.loads(CATALOG.read_text())["datasets"]
        self.model = StaticModel.from_pretrained(MODEL)
        if VECTORS.exists():
            cached = np.load(VECTORS, allow_pickle=True)
            if len(cached["ids"]) == len(self.datasets):
                self.vectors = cached["vectors"]
                return
        print("  embedding catalog (one-off, ~30s)...", file=sys.stderr)
        vecs = self.model.encode([dataset_text(d) for d in self.datasets],
                                 show_progress_bar=False)
        self.vectors = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
        np.savez_compressed(VECTORS, vectors=self.vectors,
                            ids=np.array([d["id"] for d in self.datasets]))

    def search(self, query, k=5):
        v = self.model.encode([query], show_progress_bar=False)[0]
        v = v / self.np.linalg.norm(v)
        sims = self.vectors @ v
        out = []
        for i in self.np.argsort(-sims)[:k]:
            d = dict(self.datasets[int(i)])
            d["score"] = round(float(sims[int(i)]), 3)
            out.append(d)
        return out
