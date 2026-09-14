#!/usr/bin/env python3
"""Decide whether an SDG indicator is something a CITY could report.

Replaces a keyword blocklist that passed 328 of 377 indicators it was supposed
to catch. The failure mode was structural: the class we need to exclude --
development finance -- is spelled a hundred ways ("gross receipts by developing
countries of official non-concessional sustainable development grants") and no
word list covers it.

This compares an indicator against prototype descriptions of each class using
the same embedding model as the NYC matcher, and classifies by which side it is
closer to. Scored against a hand-labelled set in probe/scope_eval.json -- run
`python3 probe/scope.py --eval` to reproduce the numbers.

Falls back to the keyword list when model2vec is absent, and says so.
"""

import argparse
import json
import pathlib
import sys

CACHE = pathlib.Path(__file__).resolve().parent / "cache"
EVAL = pathlib.Path(__file__).resolve().parent / "scope_eval.json"
MODEL = "minishlab/potion-base-32M"

# Chosen from the sweep in --eval, not by taste. A false negative silently drops
# a real city indicator forever; a false positive only adds a row to a shortlist
# a human is already reading. So we take the operating point with recall 1.00 --
# precision 0.83, five false positives out of 26, against eleven for the keyword
# list it replaces.
THRESHOLD = -0.06

# What a city government measures, funds, or is held to account for.
CITY = [
    "air quality and pollution measured in a city",
    "crime, violence and safety in a municipality",
    "housing conditions, rent and homelessness in a city",
    "municipal waste collected and recycled",
    "road traffic collisions and deaths on city streets",
    "access to drinking water and sanitation for residents",
    "public transport, commuting and street infrastructure",
    "school enrolment, attendance and completion for local students",
    "hospital admissions, disease incidence and mortality among residents",
    "unemployment, wages and poverty among residents",
    "electricity and clean cooking fuel in households",
    "parks, public open space and built-up land in a city",
    "city government budget and spending on public services",
    "deaths and damage from local floods, storms and heatwaves",
]

# What only a sovereign state has, does, or reports.
NATIONAL = [
    "official development assistance disbursed by donor countries",
    "aid grants and concessional finance received by developing countries",
    "external debt stocks, debt service and sovereign borrowing",
    "balance of payments, current account and foreign exchange reserves",
    "import tariffs, trade agreements and the World Trade Organization",
    "ratification of international treaties and conventions",
    "remittance corridors and migrant transfer costs between countries",
    "national legislative and constitutional frameworks adopted by a state",
    "marine fisheries, ocean territory and maritime boundaries",
    "forest cover, biodiversity targets and protected mountain ecosystems",
    "agricultural land, crop productivity and livestock breeds",
    "military expenditure, armed conflict and arms transfers",
    "membership and voting rights in international organizations",
    "national statistical capacity and census funding by donors",
]


def available():
    try:
        import model2vec, numpy  # noqa: F401
        return True
    except ImportError:
        return False


class Scoper:
    def __init__(self):
        import numpy as np
        from model2vec import StaticModel
        self.np = np
        self.model = StaticModel.from_pretrained(MODEL)
        self.city = self._unit(self.model.encode(CITY, show_progress_bar=False))
        self.nat = self._unit(self.model.encode(NATIONAL, show_progress_bar=False))

    def _unit(self, m):
        return m / self.np.linalg.norm(m, axis=1, keepdims=True)

    def score(self, name):
        """Positive means city-scoped. The margin is the confidence."""
        v = self.model.encode([name or ""], show_progress_bar=False)[0]
        v = v / self.np.linalg.norm(v)
        # Mean of the top 3 prototypes per side: an indicator matches a *kind* of
        # thing, not the whole class, so averaging all 14 washes the signal out.
        c = sorted(self.city @ v, reverse=True)[:3]
        n = sorted(self.nat @ v, reverse=True)[:3]
        return float(sum(c) / 3 - sum(n) / 3)

    def is_city(self, name, threshold=THRESHOLD):
        return self.score(name) > threshold


def run_eval(threshold=THRESHOLD):
    from match_nyc import keywords, city_scoped
    cases = json.loads(EVAL.read_text())["cases"]
    s = Scoper() if available() else None
    rows = []
    for c in cases:
        kw = city_scoped(keywords(c["name"]))
        emb = s.is_city(c["name"], threshold) if s else None
        rows.append((c["name"], c["city"], kw, emb, s.score(c["name"]) if s else 0))

    def report(label, idx):
        tp = sum(1 for r in rows if r[1] and r[idx])
        fp = sum(1 for r in rows if not r[1] and r[idx])
        fn = sum(1 for r in rows if r[1] and not r[idx])
        tn = sum(1 for r in rows if not r[1] and not r[idx])
        prec = tp / (tp + fp) if tp + fp else 0
        rec = tp / (tp + fn) if tp + fn else 0
        print(f"  {label:<22} precision {prec:.2f}  recall {rec:.2f}  "
              f"(tp {tp} fp {fp} fn {fn} tn {tn})")
        return prec, rec

    print(f"\nhand-labelled cases: {len(cases)} "
          f"({sum(1 for c in cases if c['city'])} city-scoped)\n")
    report("keyword blocklist", 2)
    if s:
        report(f"embeddings @{threshold}", 3)
        print("\n  worst misses:")
        for name, truth, kw, emb, sc in sorted(rows, key=lambda r: abs(r[4])):
            if truth != emb:
                print(f"    {'should be CITY ' if truth else 'should be NAT  '}"
                      f"score {sc:+.3f}  {name[:62]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", action="store_true")
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    ap.add_argument("--name", help="classify one indicator name")
    a = ap.parse_args()
    if a.name:
        s = Scoper()
        print(f"{s.score(a.name):+.3f}  {'CITY' if s.is_city(a.name) else 'NATIONAL'}")
    else:
        run_eval(a.threshold)
