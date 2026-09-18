# UN Data Commons × NYC — agent context

Hackathon project: a live Voluntary Local Review workbench bridging NYC Open Data and the
UN System Data Commons.

**Read `docs/index.md` first.** It is the project briefing and is kept current.
`docs/activity.md` is the append-only feed of what happened when.

## Hard-won rules — do not relearn these the expensive way

- **The UN graph is national-level.** NYC resolves as `geoId/3651000` but has zero UN
  observations. Any design that assumes you can look NYC up in the UN graph is wrong.
- **Discover variables through MCP, never through REST.** The MCP surface only returns governed
  `undata/` variables. REST is federated with the wider Data Commons graph and will answer for
  other publishers without warning.
- **Never guess a DCID.** The server's own instructions forbid it and a guessed DCID returns an
  empty result rather than an error, which is worse. Resolve via `search_indicators`.
- **Check coverage before designing around an indicator.** Run `probe/coverage_probe.py`.
  Series density varies from 1 observation to 300+.
- **`get_variable_metadata` silently truncates above ~10 variables per call** — it returns
  `status: None` and an empty map, not an error. Never raise `BATCH` in `probe/screen.py`
  without re-testing.
- **`get_variable_metadata` REQUIRES `entity_dcids`.** Omit it and the server answers 200 with a
  completely empty `structuredContent` — no error, no `status`, no `variables` key at all. A
  caller that trusts the shape reads that as "every variable is missing from the graph".
  `probe/launch_diff.py` did exactly this on its first run and reported all twelve crosswalk
  DCIDs as withdrawn, two days before the launch it was written to check.
- **Re-run `probe/launch_diff.py` whenever the platform might have moved**, and
  `--set-baseline` only when the new state has been read and accepted. `UNDC_ENDPOINT` /
  `UNDC_REST` override the host without a code edit. `--self-test` proves the diff still
  detects drift rather than merely failing to find it.
- **The SDG goal trees expose StatVarPeerGroups (`undata/svpg/...`), not variables.** Follow the
  `->member` arc to real DCIDs. Rewriting the prefix is DCID guessing and returns nothing.
- **"City-scoped" is not the same as "a place can hold a value for it."** `probe/scope.py` reads
  an indicator's topic and judges it municipal; it cannot see that *"extent to which countries have
  laws and regulations that guarantee…"* measures a legislature. 28 of the 67 US-silent
  "city-scoped" indicators were country-as-subject. `us_silent.py` filters them lexically.
- **A cluster is not a count.** k-means returns *k* groups whether or not *k* categories exist,
  and membership is "nearest to this centroid", not "belongs to this category". The FOIA cluster
  spanned 15 cities; only 8 publish a dataset whose title says so. Where a category can be counted
  lexically, publish the lexical count (`probe/category_gaps.py`) and let the cluster be what
  *found* it.
- **Cached embedding vectors must be matched on IDS, never on count.** A portal re-fetched later
  returns the same datasets in a different order — 24 of 45 city catalogs did — and a length check
  accepts it silently, handing every dataset another dataset's vector. Scores stay in range and
  nothing errors. `embed.Index` now compares id lists and permutes when the set matches.
- **An indicator is its own control group — never judge a value by what its unit implies.** The
  graph's `Percent` unit covers bounded proportions *and* signed growth rates and balances, so a
  flat "percentages are 0–100" rule returned 23,172 false positives. `probe/smell.py` suppresses a
  check per-indicator when it fires often enough to be structural, and compares values against the
  indicator's own 99th percentile.
- **Never gate a check on a list of unit strings.** A whitelist of percent/count/rate units
  silently discarded Mauritius' food waste going 207 → 177,570 tonnes because `WEIGHT_TN` was not
  on it. Gate on a property of the values instead.
- **Every datapoint keeps its attribution.** The platform requires it and our QA approach
  promises it.

### Denominators — the expensive ones

- **Never let a denominator resolver fall back to a default.** `probe/population.py` used to drop
  through to NYC's ACS place code when a city declared none, so Chicago and Boston both returned
  New York's 8.5M — every Chicago rate would have been 3× too low with nothing in the output
  looking wrong. It now raises. Keep it that way.
- **Eurostat `urb_cpop1` is GREATER cities, not municipalities.** It is the obvious single source
  for Europe and it is wrong here: Madrid 5,115,272 vs 3,520,396 for the municipality, Milan
  3,580,530 vs 1,399,079. Using it would push Milan rates 60% too low, silently. Denominators come
  from each city's own statistical publication.
- **A missing ACS year is a gap, never an interpolation.** There is no ACS 1-year for 2020.

### Matching — what transfers and what does not

- **A null result from the matcher is not evidence of absence.** Boston's *Vision Zero Fatality
  Records* ranked 23rd of 235 for "road traffic deaths", below a contract-award file. We wrote
  "no substantive SDG indicator matched outside NYC" and it read as a claim about the cities,
  which was false. Precision is roughly half; treat silence as untested.
- **Score document fields separately and take the max** (`dataset_head` / `dataset_body`). A
  static embedding averages every token, so 1,500 characters of programme boilerplate drown a
  title and tags that were exactly right. Concatenating everything cost NYC median rank 23 → 14
  and put Boston's right answer at 23rd instead of 1st.
- **The vector cache is keyed by model AND `REPR_VERSION`.** Change how documents are built and
  bump it, or stale vectors are silently reused with no symptom.
- **An absolute similarity cutoff does not travel between catalogs** (good matches span 0.42–0.70
  in NYC, 0.37–0.59 in Madrid), and **a per-catalog percentile cutoff is top-coded** — it keeps
  ~20% by construction, so 28 cities scored exactly 12 and the column carried no information.
  Calibrated cutoffs are for bounding one city's worksheet; fixed bars are for comparing cities.
  Neither does the other's job.
- **A z-score does not work** and was tried: against a catalog whose scores cluster near zero the
  top hit is many σ above the mean whether it is right or garbage.
- **The embedding model is chosen per catalog language.** English catalogs keep
  `potion-base-32M`; anything else gets `potion-multilingual-128M`. Swapping wholesale costs
  English accuracy (NYC median 23 → 81); using English everywhere returns literally zero for
  Madrid and Milan.

## Layout

- `docs/` — the briefing hub, served at https://sarapis.github.io/undatacommons-nyc/
- `docs/artifacts/` — generated outputs; regenerate rather than hand-edit
- `mcp/` — the benchmark MCP server, **7 tools**. `server.py` serves the graded crosswalk and
  REFUSES on pairs a human graded incomparable; `reportable_gaps`, `framework_coverage` and
  `data_quality` serve the US-silent worksheet, the category gaps and the smell-test findings from
  committed artifacts (no probe re-run needed). `smoke.py` (29 checks) asserts every figure the
  server and the demo publish against the artifacts and the pipeline that produced them.
- `probe/` — probes and the enumeration pipeline (stdlib only)
  - `corpus.py` → `screen.py` → `catalog.py` → `match_nyc.py`: enumerate the SDG corpus,
    screen for US coverage, cache the NYC catalog, propose candidates by embedding search.
    Cached in `probe/cache/`, all stages resumable.
  - Needs `pip3 install model2vec` for embedding search. Without it the matcher falls back to
    keyword overlap, which measured median rank 1535 of 2400 — worse than a coin flip.
  - `pair_probe.py`: verify both sides of every crosswalk mapping.
  - `smell.py`: plausibility checks over the corpus (689 indicators, 773k observations, one
    `get_child_observations` call each). `--recheck` re-runs the checks over cached raw
    observations and fetches nothing — always use it when changing a check. `--all` sweeps every
    base indicator rather than the 442 screened usable; it adds 0.65% more data, because 207 of
    the extra 247 hold no country observations at all.
  - `launch_diff.py`: snapshot every DCID the crosswalk expects and diff it against
    `probe/cache/launch-baseline.json`. `--set-baseline` to accept a new state (deliberately,
    never automatically); `--self-test` to prove the diff still detects drift.
  - `category_gaps.py`: counts a category two ways — how many named SDG indicators carry its
    vocabulary, and how many municipal datasets do, by city, in six languages. No clustering.
    Use it whenever a cluster is about to become a published number.
  - `us_silent.py`: the indicators the US does not report but a city could — verifies US
    absence against observations, records the peer group, proposes NYC candidates. Excludes
    country-as-subject indicators lexically; the scope classifier cannot see that
    "extent to which countries have laws…" is not a quantity a place can hold.
  - `fetch_municipal.py` → `inverse.py`: the inverse crosswalk (`--language non-en` pools every
    non-English catalog under the multilingual model; controls for it are hand-built in
    `probe/inverse_controls.json` since no city outside NYC has a graded worksheet) — cache every city catalog, then
    match each dataset to its nearest SDG indicator and cluster the far tail. Answers what
    municipal data the framework has no vocabulary for.
  - `population.py` / `denominators.py`: per-city population, from a cited source.
  - `scope.py` + `scope_eval.json`: is an indicator something a city could report?
    (embedding classifier, precision 0.83 at recall 1.00 — `python3 probe/scope.py --eval`)
  - `bootstrap.py`: generate a grading worksheet for any city in `cities/registry.json`.
  - `validate_crosswalk.py`: check the crosswalk against comparability spec v0.1.
- `cities/` — the multi-city registry, per-city worksheets and denominators
- `portals/` — the constructed inventory of city open data portals and its analysis
- `spec/` — the comparability spec's JSON Schema

## Environment

- **`git` needs `DEVELOPER_DIR=/Library/Developer/CommandLineTools`** on this machine.
  `/usr/bin/git` shims to Xcode.app, which refuses to run until someone accepts its licence
  (`sudo xcodebuild -license`). Exporting `DEVELOPER_DIR` uses the CommandLineTools toolchain and
  changes no system state.
- **`CENSUS_API_KEY` lives in a gitignored `.env`.** This repo is public. Verified absent from
  every tracked file and the full history; keep it that way.
- **Do not pipe a long background job through `tail`** — the pipeline buffers and you get no
  progress until it ends. Write to a log and poll the log.

## Conventions

Two pages, two jobs. **`docs/index.md` is current state and gets overwritten;
`docs/_posts/` is history and never does.** When a finding invalidates something in the
briefing, post an update *and* correct the briefing — a feed nobody reconciles is just a diary.

- Post updates with `./tools/new-update.sh "Short title"`, then write the body. Say what
  changed, what it revealed, and what it means next.
- Record choices in `docs/decisions.md` with the reasoning, newest first.
- Update the `Last updated` date in `docs/index.md` when you change it.
