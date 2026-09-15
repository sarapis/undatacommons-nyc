# Continue here — UN Data Commons × NYC

Written 2026-09-15. **Builders' Day is Tue 22 Sep** at Google NY; the platform goes public
**17 Sep**.

---

## 1. The one idea

**Every automated check in this project has, at least once, produced a confident answer that was
wrong — and each time a person reading the output for five minutes caught it.** Six so far:

| What passed | What was actually true |
|---|---|
| `chartable: yes` on pairs a human graded incomparable | mechanical checks overrode the grade |
| "screened 689/689" | 9 recorded; the API truncates silently above ~10 |
| "no SDG indicator matched outside NYC" | the data is there; the matcher ranked it 23rd |
| Chicago & Boston population 8,478,072 | that is New York's; the resolver fell back |
| 28 cities scoring exactly 12 | the cutoff keeps 20% by construction |
| Calgary → Gary, Indiana | substring match, denominator 20× too small |

The project's thesis and its own failure mode are the same thing. **Verify counts by printing a
table across all cases, not by testing one.** That is how four of those six were caught.

---

## 2. State — verified 2026-09-15, not recalled

Repo `/Users/devin/Antigravity/undatacommons-nyc`: **clean, 0 unpushed, on `main`.**

```bash
cd /Users/devin/Antigravity/undatacommons-nyc
python3 mcp/smoke.py                 # 8/8 passed
python3 probe/validate_crosswalk.py  # CONFORMS, 0 errors 0 warnings
python3 probe/scope.py --eval        # embeddings 0.83 precision, 1.00 recall
```

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
   are reused invisibly.
5. **Discover DCIDs through MCP, never REST**, and never guess one — a guess returns empty, not
   an error.
6. **The bootstrapper must not emit a crosswalk.** Spec v0.1 makes a grade a human judgment; it
   emits `is_crosswalk: false`.
7. **`CENSUS_API_KEY` stays out of git.** Public repo, verified clean across full history.
8. **`export DEVELOPER_DIR=/Library/Developer/CommandLineTools`** before any `git` command.

---

## 4. Waiting on the human

- **Sep 17 launch re-run.** Not a decision — just undone, and it is the one thing that could break
  the demo before the 22nd. Re-run every probe against production and diff the DCIDs.
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

1. **The Sep 17 diff.** Two days out, highest risk, cheapest insurance.
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

**Not done, stated plainly:**
- The Sep 17 re-run, the talk, and denominators for 24 non-US cities.
- No second city has been graded, so the spec has never been used by anyone but its author.
- `leedsdatamill.org`, `dati.lazio.it`, `www.opendata-hro.de` fail the catalog fetch; 3 of 70
  municipal portals are unscored.
