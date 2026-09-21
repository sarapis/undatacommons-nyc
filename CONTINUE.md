# Continue here — UN Data Commons × NYC

Written 2026-09-15, updated 2026-09-20. **Builders' Day is Tue 22 Sep** at Google NY — two days
away. The platform went public 17 Sep with zero drift.

---

## 1. The one idea

**Every automated check in this project has, at least once, produced a confident answer that was
wrong — and each time a person reading the output for five minutes caught it.** Nine so far:

| What passed | What was actually true |
|---|---|
| `chartable: yes` on pairs a human graded incomparable | mechanical checks overrode the grade |
| "screened 689/689" | 9 recorded; the API truncates silently above ~10 |
| "no SDG indicator matched outside NYC" | the data is there; the matcher ranked it 23rd |
| Chicago & Boston population 8,478,072 | that is New York's; the resolver fell back |
| 28 cities scoring exactly 12 | the cutoff keeps 20% by construction |
| Calgary → Gary, Indiana | substring match, denominator 20× too small |
| "all 12 crosswalk DCIDs missing from the graph" | `get_variable_metadata` needs `entity_dcids`; without it the server returns an empty 200 |
| 41,350 smell-test findings (5.4% of all data) | growth rates are signed by construction; an indicator is its own control group |
| inverse-crosswalk clusters, e.g. "school" = building violations | `embed.Index` reused cached vectors on a LENGTH check; 24 of 45 catalogs had re-ordered |

The project's thesis and its own failure mode are the same thing. **Verify counts by printing a
table across all cases, not by testing one.** That is how seven of those nine were caught —
including the launch diff's bug, about itself.

---

## 2. State — verified 2026-09-20, not recalled

Repo `/Users/devin/Antigravity/undatacommons-nyc`: **clean, 0 unpushed, on `main`.**

```bash
cd /Users/devin/Antigravity/undatacommons-nyc
python3 mcp/smoke.py                 # 8/8 passed
python3 probe/validate_crosswalk.py  # CONFORMS, 0 errors 0 warnings
python3 probe/scope.py --eval        # embeddings 0.83 precision, 1.00 recall
python3 probe/launch_diff.py         # 57 series + 12 variables + corpus, 0 drifted
python3 probe/launch_diff.py --self-test   # 10/10 — proves the diff can see drift
```

**The platform went public 17 Sep and nothing moved.** `launch_diff.py` that morning: 57 series,
12 variables, 689 corpus indicators, **zero drift** against the 16 Sep baseline; smoke 8/8. No
public hostname resolves even now (`undatacommons.unicc.biz`, `datacommons.un.org` both refuse),
so the pre-launch host is still the one answering.

⚠️ **That diff is 3 days old and the event is in 2.** Re-run it before Tuesday — one command,
exits non-zero on drift.

| Thing | Count | Source of truth |
|---|---:|---|
| SDG indicators enumerated | 689 | `probe/cache/corpus.json` |
| Usable on the UN side | 442 | `probe/cache/screened.json` |
| Crosswalk pairs, hand-graded | 12 | `probe/crosswalk.json` |
| US-silent indicators a place can hold | 39 | `docs/artifacts/us-silent-latest.md` |
| Demo cards / sections | 5 cards + 3 added | `demo/benchmarks.html` |
| Verified errors in UN data | 7 | `docs/findings/2026-09-16-data-quality-report.md` |
| MCP server tools | 7 | `mcp/server.py` |
| Portals surveyed / municipal | 372 / 70 | `portals/inventory.json` |
| Cities with a denominator | 27 US + Madrid + Milan | `cities/denominators.json` |

**Live and verified 200:** [briefing](https://sarapis.github.io/undatacommons-nyc/) ·
[demo](https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html) ·
[spec](https://sarapis.github.io/undatacommons-nyc/spec/) ·
[municipal table](https://sarapis.github.io/undatacommons-nyc/artifacts/municipal-latest/) ·
[activity feed](https://sarapis.github.io/undatacommons-nyc/activity/).
Artifact: `https://claude.ai/code/artifact/ffc953a4-5d1f-4666-8b0f-44db6a3dc975` (private until
shared; the Pages mirror is the one to present from).

**Inherited, not ours:** `/Users/devin/Antigravity/WeGovMarketing` has 14 dirty files dated
**28 Aug** — three weeks before this session. Untouched here. Do not tidy it as if it were ours.

---

## 3. Invariants — break these and something already fixed re-breaks

1. **A human grade vetoes every mechanical check.** `CHARTABLE_GRADES` in `pair_probe.py` and
   `mcp/server.py`. Remove it and BLOCKED pairs become charts.
2. **No denominator resolver may fall back to a default.** `probe/population.py` raises when a
   city declares no FIPS. A fallback put NYC's population on Chicago.
3. **Never interpolate a missing year.** No ACS 1-year exists for 2020; rates skip it.
4. **Bump `REPR_VERSION` in `probe/embed.py`** whenever document text changes, or stale vectors
   are reused invisibly. And **cached vectors match on IDS, never on count** — a re-fetched portal
   re-orders its catalog and a length check hands every dataset the wrong vector, silently.
5. **Discover DCIDs through MCP, never REST**, and never guess one — a guess returns empty, not
   an error.
6. **The bootstrapper must not emit a crosswalk.** Spec v0.1 makes a grade a human judgment; it
   emits `is_crosswalk: false`.
7. **`CENSUS_API_KEY` stays out of git.** Public repo, verified clean across full history.
8. **`export DEVELOPER_DIR=/Library/Developer/CommandLineTools`** before any `git` command.

---

## 4. Waiting on the human

- **Send the platform-team email.** Drafted and ready, recipient identified from Devin's own
  inbox: **Yves Jaques, yjaques@unicef.org** (UNICEF, Chief Geospatial & Computational Analytics —
  he onboarded the team and invited feedback; Benedikt Wagner is event logistics, not platform).
  Text is at `/private/tmp/.../platform-team-email.txt`, which is session-scoped and will be GONE —
  reconstruct from `docs/findings/2026-09-16-data-quality-report.md`, which carries everything.
  **I could not send it: the Gmail connector has read access only** and `create_draft` was
  refused. Needs reconnecting with write scope in claude.ai connector settings.
- **The three Builders' Day decks are UNTRACKED in `~/Antigravity/undatacommons-collab`** —
  `un-datacommons-builders-dayv1/v2/v3-unnyc.pptx`, none ever committed (`git log -- '*.pptx'` is
  empty), none gitignored. Devin's call whether they belong in git; a `git clean` would take them.
- **What the demo should be on the day.** It is NYC-only. Everything since — multi-city, the spec,
  the MCP server, the inventory — strengthens the story and appears in none of it. Grow it or keep
  it focused? Devin's call; it depends on the room.
- **No talk is being written.** Devin declined one on 17 Sep; the deck plus a live demo is the
  format. Do not restart a talk unless he asks.
- **Whether to rotate the Census key.** It was pasted in chat. Low sensitivity (free, rate-limit
  only), so probably not worth it — but it is the owner's call.
- **Collaborator access.** Devin asked to stop being prompted about GitHub usernames for Henry and
  Olivia. Do not raise it again; the repo is public and readable.

---

## 5. Candidates, ranked

1. **Re-run `launch_diff.py` before Tuesday.** Last run 17 Sep; two minutes; the only thing that
   could break the demo on the day.
2. **Read the demo end to end as a document.** Every figure is machine-asserted (32 smoke checks)
   and all 10 charts confirmed drawing, but nobody has read it as prose. Individually-true
   sentences can still be collectively confusing, and no assertion catches that.
3. **Wire more denominators.** The five most matchable cities — Bolzano 19, Madrid 16, Edmonton
   15, Calgary 15, Queensland 14 — and only Madrid has one. That is the binding constraint on
   every non-US city, and each is an afternoon of reading.
4. **Grade a second city's worksheet.** Bolzano or Madrid. Would prove the spec works for someone
   other than its author, which is the main open question about it.
5. **Not more crosswalk pairs.** Checked three domains (suicide, broadband, e-waste); all three
   had NYC-side problems. Diminishing returns.

---

## 6. Traps

**Looks broken, is deliberate:**
- `benchmark("municipal-waste")` **refuses**. The UN holds zero US observations for it; the
  refusal names `world_position` instead. Working as designed.
- Buenos Aires is `status: unreachable`, not zero candidates. Its portal closes the connection on
  anonymous `package_search`. Untested ≠ empty.
- The demo's homicide and road-death charts **break at 2020**. No ACS denominator that year. The
  gap is the point.
- Malaysia recycling 147.7% is clipped off the axis in red, not deleted. An impossible figure in
  authoritative UN data is an exhibit.
- 42 of 70 portals carry a **hand override** for city/country. The domain genuinely does not say
  that `dati.retecivica.bz.it` is Bolzano.

**Looks fine, is not:**
- **The `≥0.55` column does not rank crosswalk success.** NYC — the only city with verified pairs
  — scores middling. It measures review volume.
- **`probe/match_eval.json` is a biased sample.** Every case in it had already passed the old 0.50
  filter. It cannot tell you what a filter should reject. Do not re-tune a threshold on it without
  adding true negatives first.
- **Madrid's denominator is a snapshot**, so Madrid supports levels and not trends. The historic
  padrón (`209163-0-padron-municipal-historico`) is not wired.
- **`portals/analyze.py` re-queries all 372 portals** and overwrites the match columns. Use
  `portals/publish_table.py` to re-render without re-measuring.
- **The "roughly half the candidates are plausible" figure is my reading of eight rows**, not a
  measured precision. Directionally right, not defensible as a number.
- **`search_indicators` results move even when the graph does not.** 44 → 56 candidates between 14
  and 16 Sep with no code change, nine topics gaining and none losing. The coverage report's grade
  mix (30/9/5 → 36/11/9) moved for that reason alone. Never resolve a DCID by search at showtime.
- **The US-silent worksheet is 39, not 67.** `probe/us_silent.py`. The old 67 counted 28
  country-as-subject indicators ("extent to which countries have laws…"), which no place can hold
  a value for. The real core is 12 waste/water/wetlands indicators against DSNY and DEP series;
  three carry a single year, so level-only. All 39 verified US-absent against observations.
- **The demo now carries the three new findings**, and `mcp/smoke.py` (32 checks) asserts every
  figure on it against `screened.json`, `crosswalk.json`, `us-silent-*.json` and
  `category-gaps-*.json`. The masthead funnel had carried numbers matching no run for days because
  nothing tied it to the pipeline; it does now.
- **The inverse crosswalk runs in two language groups and they corroborate each other.**
  `probe/inverse.py` (English, 37 cities) and `--language non-en` (11 cities, multilingual model).
  Elections and COVID-19 reporting appear independently in both — disjoint cities, different
  models. Non-English controls pass 11/11 but Portuguese is the weak link (p32, p44), so the
  Brazilian portion of its tail is the least trustworthy part.
- **`screen.py`'s six-country panel is validated, not assumed.** Its `NO-DATA` grade could only
  ever mean "these six do not report it"; sweeping all 689 indicators showed 207 of the 247 it
  excluded hold **no country data at all**, and the excluded set adds 0.65% of the corpus. 442 is
  the right denominator.
- **`screened.json` row order used to be whatever the server answered in**, so two runs with
  *identical* results produced a 2,648-line diff — the noise a real change hides in. `screen.py`
  now sorts by DCID. Knock-on: `match_nyc.py` and `bootstrap.py` sort by coverage/depth with
  **non-total** keys, so input order was silently breaking ties and thus deciding which indicators
  survived `--limit`. That is now deterministic; published city worksheets were generated under
  the old arbitrary order and have not been regenerated.

- **`smell.py --recheck` needs `--all` too, or it silently narrows.** `--recheck --corpus
  corpus-all.json` without `--all` re-checked only the 442 usable set and **overwrote the
  whole-graph artifact with the smaller one**. No error. Always pass all three flags together.
- **Enumeration is entry-point dependent.** Root yields 1,661 base indicators, the 17 goal trees
  689 — but 6 are reachable from the goal trees and **not** from Root, reproducibly, though all 17
  are Root's direct children. Neither root sees everything. 689 stays correct for a VLR; never
  call it "the corpus".
- **The `portland-ocds` MCP connector is broken and NOT fixable on the box.** Its documented
  endpoint (`/mcp/mcp`) does not exist in nginx there; Postgres runs natively as superuser with
  `tenders` readable, so the "permission denied" comes from some *other* host whose URL lives in
  claude.ai settings. Full diagnosis on Hub task `cb774ead`. Portland's numbers were taken over
  SSH instead and are already in the finding.

**Not done, stated plainly:**
- Denominators for 24 non-US cities — still the binding constraint on every multi-city claim.
- The platform-team email is written but **unsent** (connector is read-only).
- The `--roots all` sweep found 2 new errors; its **MEDIUM/LOW findings are unread** — 3,844 total,
  only the 93 HIGH were triaged.
- No second city has been graded, so the spec has never been used by anyone but its author.
- `leedsdatamill.org`, `dati.lazio.it`, `www.opendata-hro.de` fail the catalog fetch; 3 of 70
  municipal portals are unscored.
