# Continue here — UN Data Commons × NYC

Written 2026-09-15, rewritten 2026-09-22 **after** Builders' Day (Google NY, 22 Sep, 10–18).
The event has happened. Nothing here is urgent any more; it is now a project with a result,
three repos, two live sites and one broken deploy pipeline.

---

## 1. The one idea

**Every automated check in this project has, at least once, produced a confident answer that was
wrong — and each time a person reading the output for five minutes caught it.** Eleven so far:

| What passed | What was actually true |
|---|---|
| `chartable: yes` on pairs a human graded incomparable | mechanical checks overrode the grade |
| "screened 689/689" | 9 recorded; the API truncates silently above ~10 |
| "no SDG indicator matched outside NYC" | the data is there; the matcher ranked it 23rd |
| Chicago & Boston population 8,478,072 | that is New York's; the resolver fell back |
| 28 cities scoring exactly 12 | the cutoff keeps 20% by construction |
| Calgary → Gary, Indiana | substring match, denominator 20× too small |
| "all 12 crosswalk DCIDs missing from the graph" | `get_variable_metadata` needs `entity_dcids`; without it, an empty 200 |
| 41,350 smell-test findings | growth rates are signed by construction; an indicator is its own control group |
| inverse-crosswalk clusters | cached vectors reused on a LENGTH check; 24 of 45 catalogs had re-ordered |
| instance load `status = SUCCESS`, exit 0 | `numObs: 0` — CSVs one directory down; the site came up on an empty DB |
| Milan updated 2,582 datasets last year | 2,445 of them share one date — a bulk re-save, not maintenance |

**Verify counts by printing a table across all cases, not by testing one.** The project's thesis
and its own failure mode are the same thing.

---

## 2. State — verified 2026-09-22 20:30, not recalled

**`git fetch` first in every repo — there is more than one committer.** Henry pushed to the
analysis repo mid-session on 18 Sep; another session pushed seven commits to the instance repo
overnight 21–22 Sep. A stale ref reports "0 unpushed" right up until the push is rejected.

| Repo | Remote | State |
|---|---|---|
| `/Users/devin/Antigravity/undatacommons-nyc` | sarapis/undatacommons-nyc | clean, pushed — the analysis |
| `/Users/devin/Antigravity/undatacommons-collab` | sarapis/undatacommons-collab | pushed; `slides/` untracked (below) |
| `/Users/devin/Antigravity/nyc-datacommons` | sarapis/nyc-datacommons | clean, pushed — the instance, owned by another session |

```bash
cd /Users/devin/Antigravity/undatacommons-nyc
python3 mcp/smoke.py                       # 33/33 — incl. all 3 demo copies identical
python3 probe/validate_crosswalk.py        # CONFORMS, 0 errors 0 warnings
python3 probe/scope.py --eval              # embeddings 0.83 precision, 1.00 recall
python3 probe/launch_diff.py               # last run 20 Sep: 57 series, 12 vars, 689 — 0 drift
python3 probe/launch_diff.py --self-test   # 10/10 — a clean diff means nothing without this
```

**Live, verified 200 on 22 Sep:**
- **https://undatacommons.sarapis.org** — collab site. `/` 302s to `/start/`; the overview is
  `/summary/`; the errors index is `/addendum-errors-in-the-un-data/`; the demo is `/demo/`.
- **https://commons.databook.nyc** — NYC's own Data Commons. **16 variables, 572 observations**,
  each read back over the API against its CSV. Hetzner cpx32, €41.99/mo.
- **https://sarapis.github.io/undatacommons-nyc/** — the briefing (`docs/index.md`) and demo.

| Thing | Count | Source of truth |
|---|---:|---|
| SDG base indicators (goal trees) / whole graph | 689 / 1,661 | `probe/cache/corpus*.json` |
| Usable on the UN side / US-silent | 442 / 130 | `probe/cache/screened.json` |
| Crosswalk pairs, hand-graded | 12 | `probe/crosswalk.json` |
| Verified errors in UN data (of 3,844 flags) | 7 | `docs/findings/2026-09-16-data-quality-report.md` |
| Portals surveyed / city-and-regional | 372 / 70 | `portals/inventory.json` |
| Denominators wired (of the 70) | 29 = 27 ready + 2 | `cities/denominators.json` |
| MCP server tools | 7 | `mcp/server.py` |

**The deck that was presented is Google Slides**, not a file in any repo:
`https://docs.google.com/presentation/d/1Or6GLDXNXZtwHwVSniaQbWuND81brsWxgJktVd_z5co` — Devin
imported it and shared it at 22:19 on 21 Sep and again at 14:48 on the day. The repo's
`un-datacommons-builders-dayv4-unnyc.pptx` was rebuilt at 20:31 on 22 Sep to correct slide 9
(11→16 variables; "roughly 3 loadable" → zero) and a slide-11 punchline that was 83 chars
against an 80 cap. **Those corrections are not in the Google Slides deck.**

**Inherited, not ours:** `/Users/devin/Antigravity/WeGovMarketing` has 14 dirty files dated 28 Aug.

---

## 3. Invariants — break these and something already fixed re-breaks

1. **A human grade vetoes every mechanical check** — `CHARTABLE_GRADES` in `probe/pair_probe.py`,
   `CHARTABLE` in `mcp/server.py` (two names, one rule; `smoke.py` asserts "poverty refused").
   Remove either and BLOCKED pairs become charts.
2. **No denominator resolver falls back to a default** — `probe/population.py` raises. A fallback
   put NYC's population on Chicago.
3. **Never interpolate a missing year.** No ACS 1-year for 2020; rates skip it. The instance
   carries no 2020 point either.
4. **Bump `REPR_VERSION` in `probe/embed.py`** when document text changes; cached vectors match
   on **ids, never count**.
5. **Discover DCIDs through MCP, never REST; never guess one** — a guess returns empty, not error.
6. **The bootstrapper never emits a crosswalk** — spec v0.1, `is_crosswalk: false`.
7. **The demo exists in three copies** — enforced by `smoke.py` ("collab site's demo copy
   identical"). Edit one, edit all three.
8. **The deck is generated.** Edit `undatacommons-collab/deck-v4-text.md`, run
   `tools/build-deck.js`. Editing the `.pptx` is overwritten on the next build.
9. **`CENSUS_API_KEY` stays out of git** — public repo, verified clean across history.
10. **`export DEVELOPER_DIR=/Library/Developer/CommandLineTools`** before any `git`.

---

## 4. Waiting on the human

- **CI deploy for the collab site has never succeeded in its last 40 runs.** The gate passes;
  the Deploy step fails because `CLOUDFLARE_API_TOKEN` is unset (`gh secret list` is empty). Every
  deploy since 19 Sep has been manual. Needs a token with Workers Scripts:Edit on account
  `a8e2fa072ede7a6389e8db8cad00f774`, then `gh secret set CLOUDFLARE_API_TOKEN` in the collab repo.
  **A credential — not ours to create.** Until then: `npm run build && npx wrangler deploy`.
- **The platform-team email is still unsent** (checked Gmail 22 Sep: the only mail to Yves Jaques,
  yjaques@unicef.org, is a cc on logistics). The substance is the data-quality report and the
  addendum page, both published. The Gmail connector is read-only.
- **Whether to carry slide 9/11's corrections into the Google Slides deck.** It is the copy people
  now hold; the repo `.pptx` is not.
- **`undatacommons-collab/slides/` — commit or discard?** A one-slide "THE CONTEXT" deck
  (`project-context.js` + `.pptx`), built at 14:25 on the day by another session from tokens read
  out of the v4 deck — 23 minutes before the Google Slides was re-shared, so probably presented.
  Untracked; its own generator, separate from `tools/build-deck.js`.
- **No talk is being written** (declined 17 Sep). **Do not raise GitHub collaborator access**
  for Henry and Olivia again — asked to stop.

---

## 5. Candidates, ranked

1. **Fix CI deploy** (above) — otherwise every push to collab silently fails to publish, and the
   green commit looks like success.
2. **Read the demo end to end as prose.** 33 checks assert every figure; nothing asserts that
   individually-true sentences add up to a clear page.
3. **Put the comparability caveat on the chart.** The instance carries each variable's grade and
   reason into the graph and shows them on `/browser/<var>` — and *not* in the chart's "About
   this data". That is the one gap between what this project argues and what the platform does.
4. **Grade a second city** (Bolzano or Madrid). The spec has never been used by anyone but its
   author — the main open question about it.
5. **Wire more denominators.** 41 of 70 portals cannot turn a count into a rate. Each city is an
   afternoon of reading its own statistical publication.

---

## 6. Traps

**Looks broken, is deliberate:**
- `benchmark("municipal-waste")` **refuses** — zero US observations; names `world_position`.
- Buenos Aires is `status: unreachable`, not zero — its portal closes anonymous `package_search`.
- Homicide and road-death series **break at 2020** everywhere, including the instance. No ACS.
- Malaysia's 147.7% recycled is clipped off the demo axis in red, and **not counted** among the
  seven errors — a share above 100% can be real (Kuwait's 3,850% water stress is).
- 42 of 70 portals carry a hand override for city/country; the domain genuinely does not say so.

**Looks fine, is not:**
- **`/` on the collab site is a 302 to `/start/`.** A grep of `/` for summary text finds nothing
  and reads as "not deployed". The summary is `/summary/`.
- **`level == "city"` in `portals/inventory.json` gives 58, not 70.** The published 70 is "city and
  regional". A filter on level makes a correct figure look wrong.
- **Portal freshness counts lie without a date histogram.** Milan's 2,582 "updated last year" is
  94% one day. Subtract each portal's busiest day, or count distinct days (NYC: 187).
- **The collab site 403s urllib without a browser User-Agent**; curl works. Not an outage.
- **The instance API: `date=all` returns an empty `byEntity`; `date=LATEST` works.** Not missing data.
- **The ≥0.55 column does not rank crosswalk success** — it measures review volume. NYC, the only
  verified city, scores middling.
- **`probe/match_eval.json` is a biased sample** — every case already passed the old 0.50 filter.
  Add true negatives before re-tuning any threshold on it.
- **`search_indicators` results move when the graph does not** (44 → 56 candidates, 14–16 Sep).
  Never resolve a DCID by search at showtime; hardcode human-resolved ones.
- **`smell.py --recheck` needs `--all` too**, or it re-checks the 442 and overwrites the whole-graph
  artifact with the smaller one, silently.
- **Enumeration is entry-point dependent** — 6 indicators reachable from the goal trees and not
  from Root. 689 is right for a VLR; never call it "the corpus".
- **The US-silent twelve yielded zero loadable NYC series**, not the "about three" once estimated —
  "hazardous waste" and "groundwater" each return zero datasets in the whole NYC catalog.
- **Madrid's denominator is a snapshot** — levels, not trends.
- **`portals/analyze.py` re-queries all 372 portals** and overwrites match columns; use
  `portals/publish_table.py` to re-render without re-measuring.
- **The `portland-ocds` MCP connector is broken off-box** (its URL lives in claude.ai settings,
  not nginx). Portland's figures were taken over SSH. Hub task `cb774ead`.
- **Deck build: the generator's `node_modules` live in a session scratchpad**, not the repo.
  `npm install pptxgenjs react-icons react react-dom sharp` into a scratch dir and run there.

**Not done, stated plainly:**
- The whole-graph sweep's **MEDIUM/LOW findings are unread** — only the 93 HIGH of 3,844 triaged.
- **No second city graded**; no cross-city benchmark computed. Every multi-city claim is diagnosis.
- `leedsdatamill.org`, `dati.lazio.it`, `www.opendata-hro.de` fail the catalog fetch; unscored.
- The instance was load-tested at 10-way concurrency once. One page render 502'd. Not public-grade.

---

## For the next session

Paste this to start:

> Pick up the UN Data Commons × NYC project. Builders' Day (22 Sep) is over. Read
> `/Users/devin/Antigravity/undatacommons-nyc/CONTINUE.md` first — it is the only required
> reading, and its section 2 says which of the three repos holds what.
>
> Run `git fetch` in any repo before trusting its state; each has more than one committer.
> Read `/Users/devin/Antigravity/undatacommons-collab/CLAUDE.md` only if you touch the site or the
> deck, and `/Users/devin/Antigravity/nyc-datacommons/CLAUDE.md` only if you touch the instance.
>
> Do not write a handoff, continuation prompt, or session record unless I ask for
> `/handoff`. End your turn with what you did and what you recommend next.
