#!/usr/bin/env python3
"""Stage 3 — propose NYC Open Data candidates for each screened UN indicator.

This is the step that removes my own bias from the crosswalk. The first eleven
pairs were chosen by imagining what NYC might publish, so they could only ever
confirm my assumptions. Here the UN corpus drives: every indicator with a usable
US series gets searched for, including the ones I would never have thought of.

Output is a RANKED SHORTLIST FOR HUMAN REVIEW, not a set of mappings. Scores
measure term overlap, which is a decent way to surface a candidate and a
terrible way to decide comparability -- the waste pair has agreeing units and is
still not apples to apples. Judgment stays human, as with the grade veto in
pair_probe.py.

Usage:  python3 probe/match_nyc.py [--limit N] [--min-score 0.2]
Reads probe/cache/screened.json, writes docs/artifacts/candidates-<date>.md.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nyc  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "probe" / "cache"
ARTIFACTS = ROOT / "docs" / "artifacts"

# Words that carry no retrieval signal here: statistical boilerplate that
# appears in most indicator names, plus ordinary English stopwords.
STOP = set("""a an the of in on for to and or by with per from as at is are be
proportion percentage number total rate ratio population people index value
estimated average annual mean level levels among all both which that this
national countries country year years age sex data measure share""".split())


# Many SDG indicators are macroeconomic or nation-state concepts that no city
# publishes and none ever will -- balance of payments, ODA, refugees by country
# of origin, tariffs. Matching them against a municipal catalog can only produce
# false positives, so they are excluded before searching rather than filtered out
# of the results afterwards. This list is a judgment call and belongs under review.
NOT_CITY_SCOPED = set("""gdp tariff tariffs exports imports remittances balance
payments account debt fiscal monetary currency sovereign oda aid donor recipient
refugees asylum migrant seats parliament treaty ratified convention signatory
multilateral bilateral trade wto imf armed weapons military nuclear seizures
territorial maritime marine ocean fisheries fish forest forests mountain
biodiversity ecosystems species agricultural agriculture livestock crop crops
rural farmers pastoral""".split())

# A single coincidental word match is not a candidate. "Domestic material
# consumption" scoring against "Mayor's Office to End Domestic Violence" on the
# word "domestic" is the failure this guards against.
MIN_MATCHED_TERMS = 2
MIN_COVERAGE = 0.5


def city_scoped(terms):
    return not (set(terms) & NOT_CITY_SCOPED)


def keywords(name):
    words = re.findall(r"[a-z0-9]+", (name or "").lower())
    return [w for w in words if w not in STOP and len(w) > 2]


def score(terms, dataset):
    """Term overlap, requiring genuine multi-term agreement.

    Returns 0 for anything that does not clear both an absolute floor (at least
    two distinct indicator terms present) and a proportional one. Term overlap
    is a weak signal and this only makes it less wrong -- the output is still a
    shortlist for a human, never a mapping.
    """
    hay = f"{dataset.get('name','')} {dataset.get('description','')}".lower()
    uniq = set(terms)
    if not uniq:
        return 0.0
    hits = sum(1 for t in uniq if t in hay)
    coverage = hits / len(uniq)
    if hits < MIN_MATCHED_TERMS or coverage < MIN_COVERAGE:
        return 0.0
    base = coverage
    # A dataset stale for years is a weaker candidate even if it matches well.
    updated = (dataset.get("updatedAt") or "")[:4]
    if updated.isdigit() and int(updated) >= dt.date.today().year - 2:
        base += 0.1
    if (dataset.get("name") or "").upper().startswith("ARCHIVED"):
        base -= 0.5
    return round(min(base, 1.0), 3)


def search(terms, limit=5):
    if not terms:
        return []
    q = " ".join(terms[:6])
    try:
        d = nyc._get(nyc.CATALOG, {"domains": nyc.DOMAIN, "q": q, "limit": limit})
    except nyc.NYCError as exc:
        print(f"  ! {exc}", file=sys.stderr)
        return []
    return [r.get("resource", {}) for r in (d.get("results") or [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--min-score", type=float, default=0.2)
    args = ap.parse_args()

    data = json.loads((CACHE / "screened.json").read_text())
    green = [r for r in data["indicators"] if r.get("grade") == "GREEN"]
    green.sort(key=lambda r: -(r.get("n_obs") or 0))
    if args.limit:
        green = green[:args.limit]

    existing = {p["un"]["dcid"].split(".")[0]
                for p in json.loads((ROOT / "probe" / "crosswalk.json").read_text())["pairs"]}

    results, skipped = [], []
    for i, ind in enumerate(green, 1):
        terms = keywords(ind.get("name"))
        if not city_scoped(terms):
            skipped.append(ind)
            continue
        cands = []
        for ds in search(terms):
            sc = score(terms, ds)
            if sc >= args.min_score:
                cands.append({"id": ds.get("id"), "name": ds.get("name"),
                              "updated": (ds.get("updatedAt") or "")[:10], "score": sc})
        cands.sort(key=lambda c: -c["score"])
        results.append({"indicator": ind, "candidates": cands[:3],
                        "already_mapped": ind["dcid"] in existing})
        if i % 25 == 0:
            print(f"  matched {i}/{len(green)}", file=sys.stderr)
        time.sleep(0.25)

    with_c = [r for r in results if r["candidates"]]
    new = [r for r in with_c if not r["already_mapped"]]

    today = dt.date.today().isoformat()
    md = ["---", "layout: default", f"title: Crosswalk candidates — {today}", "---", "",
          f"# Crosswalk candidates — {today}", "",
          f"Every SDG indicator with a usable US series ({len(green)} of 689), searched against "
          "the NYC Open Data catalog.", "",
          f"{len(skipped)} were excluded before searching as inherently national "
          "(balance of payments, ODA, treaties, fisheries and similar) — a city does not "
          "publish them and matching could only yield false positives.", "",
          "**This is a shortlist for human review, not a set of mappings.** The score is term "
          "overlap — good for surfacing a candidate, useless for deciding comparability. "
          "Promoting a row into `probe/crosswalk.json` means writing the grade and the reason "
          "by hand.", "",
          f"- {len(green)} indicators screened GREEN on the UN side",
          f"- {len(with_c)} have at least one plausible NYC dataset",
          f"- **{len(new)} are not yet in the crosswalk**", "",
          "| Score | SDG indicator | UN obs | Candidate NYC dataset | Updated |",
          "|---|---|---:|---|---|"]
    for r in sorted(new, key=lambda r: -r["candidates"][0]["score"])[:60]:
        ind, top = r["indicator"], r["candidates"][0]
        md.append(f"| {top['score']} | {(ind.get('name') or '')[:58]} "
                  f"(`{ind['dcid'].split('/')[-1]}`) | {ind.get('n_obs')} | "
                  f"{(top['name'] or '')[:44]} (`{top['id']}`) | {top['updated']} |")
    md += ["", f"*Showing the top 60 of {len(new)} unmapped candidates. "
           f"Regenerate with `python3 probe/match_nyc.py`.*", ""]

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / f"candidates-{today}.md").write_text("\n".join(md))
    (ARTIFACTS / "candidates-latest.md").write_text("\n".join(md))
    (CACHE / "candidates.json").write_text(json.dumps(
        {"generated": today, "results": results}, indent=1))
    print(f"\n{len(green)} GREEN · {len(skipped)} not city-scoped · "
          f"{len(with_c)} with candidates · {len(new)} unmapped")
    print(f"wrote docs/artifacts/candidates-{today}.md")


if __name__ == "__main__":
    main()
