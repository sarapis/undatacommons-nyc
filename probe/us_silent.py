#!/usr/bin/env python3
"""The indicators the United States does not report, and NYC could.

The asymmetry this repo keeps circling: the UN graph is national-level, so NYC
can only ever be compared against countries -- and for 130 of the 442 usable SDG
indicators the United States reports nothing at all. On those, "NYC vs the US" is
not a weaker comparison than "NYC vs the world". It is the only one available,
and the US is not in it.

That is not a gap. It is the single place where a city has something to say
internationally that its own country does not.

WHAT THIS PRODUCES. One row per indicator: whether the US really is silent
(checked against observations, not against the screening proxy), how many
countries do report it and over what years -- that is the peer group NYC would
be placed among -- and the NYC datasets the matcher proposes. It is a worksheet
for a human, never a crosswalk: under comparability spec v0.1 a grade is a human
judgment, so every row here is `graded: false`.

THE SCREEN IS A PROXY AND IS CHECKED. `screen.py` decides "the US reports this"
from `entityCoverage` on a six-country panel. This verifies each claim against
the actual country observations and reports any disagreement rather than
inheriting it.

Usage:  python3 probe/us_silent.py [--limit N] [--candidates 3]
Writes docs/artifacts/us-silent-<date>.{json,md}.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "probe"))
import embed                                   # noqa: E402
import scope                                   # noqa: E402

CACHE = ROOT / "probe" / "cache"
ARTIFACTS = ROOT / "docs" / "artifacts"
SCREENED = CACHE / "screened.json"
RAW = CACHE / "smell-raw.json"
US = "country/USA"
USABLE = ("GREEN", "AMBER", "RANK-ONLY")

# A peer group this small cannot place a city anywhere meaningful, whatever the
# indicator says. Stated as a column rather than used as a filter.
THIN_PEER_GROUP = 15

# Indicators whose SUBJECT is a country, not a place that can hold a value.
# "Extent to which countries have laws and regulations that guarantee..." is not
# a quantity New York City can have; the question is whether a national
# legislature passed something. The scope classifier cannot see this -- it reads
# the topic (health, water, education) and judges it municipal -- so 25 of the
# first run's 67 were country-as-subject, 18 of them one family of SDG 5.6.2
# legal provisions, every one of which the matcher paired with NYC's "Local Law
# 37/2011" on the token "Law".
#
# Lexical, deliberately: this is a property of how the indicator is phrased, and
# a rule that can be read and argued with beats a classifier that cannot.
# Note "extent to which" (a country's policy) versus "extent of" (a physical
# quantity, e.g. human-made wetlands) -- only the first is excluded.
COUNTRY_SUBJECT = re.compile(
    r"^(countries\b|number of countries|proportion of countries|extent to which\b|"
    r"degree of implementation|level of implementation|countries that\b|countries with\b|"
    r"number of (least developed|recipient)|total (inbound|outbound)\b|"
    r"international financial flows|monetary amount|amount of tracked|dollar value|"
    r"official (flows|development assistance)|net outbound)", re.I)

# Good NYC matches measured on the hand-verified pairs span 0.42-0.70. Below
# this a proposal is noise and is labelled so rather than printed as a finding.
CANDIDATE_FLOOR = 0.45


def world_coverage(raw, dcid):
    """Who reports this, over what years -- straight from the cached sweep."""
    r = raw.get(dcid)
    if not r:
        return None
    rows = [(p, str(d)[:4], v) for p, d, v in ((r.get("data") or {}).get("rows") or [])
            if v is not None]
    if not rows:
        return {"countries": 0, "n_obs": 0, "us_obs": 0, "first": None, "last": None,
                "unit": None}
    years = sorted({int(y) for _, y, _ in rows if y.isdigit()})
    src = r.get("sourceMetadata") or {}
    return {"countries": len({p for p, _, _ in rows}), "n_obs": len(rows),
            "us_obs": sum(1 for p, _, _ in rows if p == US),
            "first": years[0] if years else None, "last": years[-1] if years else None,
            "unit": (src.get("unit") or "").split("UNIT_MEASURE-")[-1],
            "provenance": src.get("provenanceUrl")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--candidates", type=int, default=3)
    args = ap.parse_args()

    rows = json.loads(SCREENED.read_text())["indicators"]
    silent = [r for r in rows if r.get("grade") in USABLE
              and "us_reports" in r and not r["us_reports"]]
    scoper = scope.Scoper()
    classified = [r for r in silent if scoper.is_city(r["name"])]
    country_subject = [r for r in classified if COUNTRY_SUBJECT.match(r["name"])]
    city = [r for r in classified if not COUNTRY_SUBJECT.match(r["name"])]
    if args.limit:
        city = city[:args.limit]
    print(f"{len(silent)} US-silent usable -> {len(classified)} city-scoped by the "
          f"classifier -> {len(city)} after removing {len(country_subject)} "
          f"country-as-subject", file=sys.stderr)

    raw = json.loads(RAW.read_text()) if RAW.exists() else {}
    index = embed.Index() if embed.available() else None

    out, disagreements = [], []
    for i, r in enumerate(city, 1):
        cov = world_coverage(raw, r["dcid"])
        # The screen said the US does not report this. Check it against the
        # observations rather than trusting the panel that produced the flag.
        if cov and cov["us_obs"]:
            disagreements.append({"dcid": r["dcid"], "name": r["name"],
                                  "us_obs": cov["us_obs"]})
        cands = []
        if index:
            for d in index.search(r["name"], k=args.candidates):
                cands.append({"id": d.get("id"), "name": d.get("name"),
                              "score": d.get("score"), "z": d.get("z")})
        out.append({"dcid": r["dcid"], "name": r["name"], "grade": r["grade"],
                    "depth": r.get("depth"), "unit": r.get("unit"),
                    "first_year": r.get("first_year"), "latest_year": r.get("latest_year"),
                    "world": cov, "nyc_candidates": cands, "graded": False})
        print(f"  {i}/{len(city)} {r['dcid']:<34}"
              f"{(cov or {}).get('countries', 0):>4} countries", file=sys.stderr)

    today = dt.date.today().isoformat()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    payload = {"generated": today, "us_silent_usable": len(silent),
               "classifier_positive": len(classified),
               "country_subject_removed": [{"dcid": r["dcid"], "name": r["name"]}
                                           for r in country_subject],
               "city_scoped": len(out), "thin_peer_group": THIN_PEER_GROUP,
               "candidate_floor": CANDIDATE_FLOOR,
               "screen_disagreements": disagreements, "indicators": out,
               "is_crosswalk": False}
    (ARTIFACTS / f"us-silent-{today}.json").write_text(json.dumps(payload, indent=1))
    text = render(payload)
    (ARTIFACTS / f"us-silent-{today}.md").write_text(text)
    (ARTIFACTS / "us-silent-latest.md").write_text(text)

    usable_rows = [r for r in out if (r["world"] or {}).get("countries", 0) >= THIN_PEER_GROUP]
    weak = [r for r in out if not r["nyc_candidates"]
            or r["nyc_candidates"][0]["score"] < CANDIDATE_FLOOR]
    print(f"\n{len(out)} place-measurable indicators the US does not report "
          f"({len(country_subject)} country-as-subject rows removed)")
    print(f"{len(weak)} have no candidate above {CANDIDATE_FLOOR}")
    print(f"{len(usable_rows)} have a peer group of {THIN_PEER_GROUP}+ countries")
    if disagreements:
        print(f"\n{len(disagreements)} DISAGREE with the screen -- the US does have "
              f"observations for these:")
        for d in disagreements:
            print(f"   {d['us_obs']:>4} obs  {d['dcid']:<32}{d['name'][:52]}")
    print(f"wrote docs/artifacts/us-silent-{today}.md")
    return 0


def render(o):
    inds = sorted(o["indicators"],
                  key=lambda r: -((r["world"] or {}).get("countries") or 0))
    strong = [r for r in inds if (r["world"] or {}).get("countries", 0) >= o["thin_peer_group"]]
    md = ["---", "layout: default", f"title: Indicators the US does not report — {o['generated']}",
          "---", "",
          "# What NYC can say internationally that the United States cannot", "",
          "The UN graph is national-level: a city can only ever be placed against countries. "
          f"For **{o['us_silent_usable']} of the 442 usable SDG indicators the United States "
          "reports nothing at all** — and on those, *NYC vs the US* is not a weaker comparison "
          "than *NYC vs the world*. It is the only one available, and the US is not in it.", "",
          f"Of those, **{o['classifier_positive']} are judged city-scoped** by the embedding "
          "classifier in `probe/scope.py` — and **"
          f"{len(o['country_subject_removed'])} of them are not**, because their subject is a "
          "*country* rather than a place that can hold a value. "
          f"**{o['city_scoped']} survive** and are listed below.", "",
          f"**{len(strong)} have a peer group of {o['thin_peer_group']}+ reporting countries**, "
          "which is the column that decides whether a placement means anything. The rest are "
          "listed too, with their true count.", "",
          "> **This is a worksheet, not a crosswalk.** Under "
          "[comparability spec v0.1](https://sarapis.github.io/undatacommons-nyc/spec/) a grade "
          "is a human judgment, so every row here is `graded: false`. The NYC candidates are "
          "proposals from an embedding matcher whose precision on hand-read lists is roughly "
          "half.", ""]

    if o["country_subject_removed"]:
        fams = {}
        for r in o["country_subject_removed"]:
            fams[r["name"][:52]] = fams.get(r["name"][:52], 0) + 1
        md += ["## Removed: the subject is a country, not a place", "",
               "The scope classifier reads an indicator's *topic* — health, water, education — "
               "and judges it municipal. It cannot see that *\"extent to which countries have "
               "laws and regulations that guarantee…\"* is not a quantity a city can have. "
               f"**{len(o['country_subject_removed'])} rows** were removed on a lexical rule, "
               "which is stated here so it can be argued with:", "",
               "| Count | Indicator family |", "|---:|---|"]
        for name, n in sorted(fams.items(), key=lambda kv: -kv[1]):
            md.append(f"| {n} | {name} |")
        md += ["", "Eighteen are one family — the SDG 5.6.2 legal provisions — and the matcher "
               "paired every one of them with NYC's *Local Law 37/2011 Temporary Housing "
               "Assistance*, on the token \"Law\". A worksheet that shipped them would have "
               "wasted a reviewer's afternoon before they reached anything real.", ""]

    if o["screen_disagreements"]:
        md += ["## The screen disagreed with the observations", "",
               "`screen.py` decides *does the US report this* from `entityCoverage` on a "
               "six-country panel. Checked against the actual observations, these rows have US "
               "data after all and should be struck from the list:", "",
               "| Indicator | US observations |", "|---|---:|"]
        for d in o["screen_disagreements"]:
            md.append(f"| {d['name'][:72]} (`{d['dcid'].rsplit('/', 1)[-1]}`) | {d['us_obs']} |")
        md.append("")
    else:
        md += ["Every row below was re-checked against the country observations: **none of "
               "them has a single United States datapoint.** The screening proxy and the data "
               "agree.", ""]

    md += ["## The worksheet", "",
           "| Indicator | SDG series | Countries | Years | Unit | Best NYC candidate |",
           "|---|---|---:|---|---|---|"]
    for r in inds:
        w = r["world"] or {}
        # One observation cannot carry a trend -- the lesson that killed road
        # safety as our headline demo. A single-year indicator supports a level
        # comparison and nothing more, and says so here.
        if not w.get("first"):
            yrs = "—"
        elif w["first"] == w["last"]:
            yrs = f"**{w['first']} only**"
        else:
            yrs = f"{w['first']}–{w['last']}"
        c = r["nyc_candidates"][0] if r["nyc_candidates"] else None
        if not c:
            cand = "—"
        elif c["score"] < o["candidate_floor"]:
            cand = f"*{c['name'][:34]} ({c['score']}, below floor)*"
        else:
            cand = f"{c['name'][:38]} ({c['score']})"
        n = w.get("countries") or 0
        mark = "" if n >= o["thin_peer_group"] else " ⚠"
        md.append(f"| {r['name'][:62]} | `{r['dcid'].rsplit('/', 1)[-1]}` | {n}{mark} | "
                  f"{yrs} | `{(w.get('unit') or '')[:22]}` | {cand} |")
    single = [r for r in inds if (r["world"] or {}).get("first")
              and r["world"]["first"] == r["world"]["last"]]
    md += ["", f"⚠ = fewer than {o['thin_peer_group']} reporting countries; a placement among "
           "them says little. **A single year** supports a level comparison and not a trend — "
           f"{len(single)} of these have one year only, which is the finding that removed road "
           "safety as our headline demo. A candidate *in italics* scores below "
           f"{o['candidate_floor']}, the floor under which a proposal is noise.", ""]

    md += ["## The strongest rows, in detail", ""]
    for r in strong[:20]:
        w = r["world"]
        md += [f"### {r['name']}", "",
               f"`{r['dcid']}` · **{w['countries']} countries** · {w['first']}–{w['last']} · "
               f"{w['n_obs']:,} observations · unit `{w.get('unit')}` · "
               f"screened {r['grade']}", ""]
        if r["nyc_candidates"]:
            md.append("Candidate NYC datasets (proposals, ungraded):\n")
            for c in r["nyc_candidates"]:
                md.append(f"- **{c['name']}** — `{c['id']}`, score {c['score']}, z {c['z']}")
        else:
            md.append("*No NYC candidate proposed.*")
        md.append("")

    md += ["## Reproducing", "", "```bash", "python3 probe/us_silent.py", "```", "",
           "Reads `probe/cache/screened.json` and the cached corpus sweep in "
           "`probe/cache/smell-raw.json`; no network calls.", ""]
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    sys.exit(main())
