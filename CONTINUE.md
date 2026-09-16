# Continue here — UN Data Commons × NYC

Written 2026-09-15, updated 2026-09-16. **Builders' Day is Tue 22 Sep** at Google NY; the
platform goes public **17 Sep** — tomorrow.

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

## 2. State — verified 2026-09-16, not recalled

Repo `/Users/devin/Antigravity/undatacommons-nyc`: **clean, 0 unpushed, on `main`.**

```bash
cd /Users/devin/Antigravity/undatacommons-nyc
python3 mcp/smoke.py                 # 8/8 passed
python3 probe/validate_crosswalk.py  # CONFORMS, 0 errors 0 warnings
python3 probe/scope.py --eval        # embeddings 0.83 precision, 1.00 recall
python3 probe/launch_diff.py         # 57 series + 12 variables + corpus, 0 drifted
python3 probe/launch_diff.py --self-test   # 10/10 — proves the diff can see drift
```

**The pre-launch pass is done (16 Sep).** Every probe re-run against the live deployment and
diffed against 14 Sep: 689 base indicators, 6,025 variant DCIDs, 689 screened indicators, 57
crosswalk series and 12 crosswalk variables — **all identical**. The *search surface* moved (44 →
56 coverage candidates, nine of fifteen topics, none lost), the graph did not. See
`docs/_posts/2026-09-16-the-launch-diff-and-the-bug-it-found-in-itself.md`.

| Thing | Count | Source of truth |
|---|---:|---|
| SDG indicators enumerated | 689 | `probe/cache/corpus.json` |
| Usable on the UN side | 442 | `probe/cache/screened.json` |
| Crosswalk pairs, hand-graded | 12 | `probe/crosswalk.json` |
| Demo cards | 5 | `demo/benchmarks.html` |
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

- **Sep 17 launch re-run — now one command, and still undone because the launch is tomorrow.**
  After the platform goes public: `python3 probe/launch_diff.py` (exits non-zero on any drift)
  then `python3 mcp/smoke.py`. If the public deployment answers on a different host, set
  `UNDC_ENDPOINT` / `UNDC_REST` — no code edit. Only run `--set-baseline` after *reading* the new
  state and accepting it; re-baselining on every run is how a checker reports "no change" forever.
  As of 16 Sep no public hostname resolves (`undatacommons.unicc.biz`, `datacommons.un.org` both
  refuse), so which host serves the public deployment is a question for the organizers.
- **What the demo should be on the day.** It is NYC-only. Everything since — multi-city, the spec,
  the MCP server, the inventory — strengthens the story and appears in none of it. Grow it or keep
  it focused? Devin's call; it depends on the room.
- **The talk is unwritten.** 5–15 minutes, single track.
- **Whether to rotate the Census key.** It was pasted in chat. Low sensitivity (free, rate-limit
  only), so probably not worth it — but it is the owner's call.
- **Collaborator access.** Devin asked to stop being prompted about GitHub usernames for Henry and
  Olivia. Do not raise it again; the repo is public and readable.

---

## 5. Candidates, ranked

1. **The Sep 17 diff — run it, it is one command now.** The harness and the pre-launch baseline
   are in place; what remains is running it once the platform is public.
2. **The talk.** Five surprises, already written up on the feed; the road-deaths inversion and the
   Malaysia 147.7% recycling figure are the two that land.
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

**Not done, stated plainly:**
- The post-launch run of `launch_diff.py` (the platform is not public until 17 Sep), the talk, and
  denominators for 24 non-US cities.
- No second city has been graded, so the spec has never been used by anyone but its author.
- `leedsdatamill.org`, `dati.lazio.it`, `www.opendata-hro.de` fail the catalog fetch; 3 of 70
  municipal portals are unscored.
