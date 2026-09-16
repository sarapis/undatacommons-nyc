---
layout: default
nav_id: summary
title: Project briefing
---

# UN Data Commons × NYC — project briefing

**Last updated: 2026-09-16** · Team: Devin, Henry, Olivia · [Repo](https://github.com/sarapis/undatacommons-nyc)

## The demo

**[Eleven Pairs, Three Charts](https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html)** — three comparisons that hold with
provenance and grade on every card, then the eight that fail and why. Each card also places NYC
among **every reporting country** in 2019. Public, no sign-in.

The headline finding: NYC ranks **#5 of 186** on city air quality, **#18 of 196** on road deaths
(four times safer than the US), and **#85 of 137** on homicide. A fifth card covers municipal
waste — an indicator the **US does not report at all**, where the caveat reverses the reading.
Against the US, NYC's homicide trend reads as a success story; against the world it sits in the
bottom half. Same number, different comparator, opposite conclusion.

## Beyond NYC

The pipeline runs against **any city** on Socrata or CKAN
([`cities/`](https://github.com/sarapis/undatacommons-nyc/tree/main/cities)). Two blockers found
in the first five-city run are now fixed, and the honest summary is that **the plumbing
generalises and the recommender is serviceable rather than good**.

**Language.** Madrid and Milan returned nothing until a multilingual model was added, now chosen
per catalog language. It is a trade-off, not an upgrade: on the NYC ground truth the English model
ranks the correct dataset at median **23** and the multilingual one at **81**, so English cities
keep the English model.

**Threshold.** An absolute similarity cutoff cannot travel — good matches span 0.42–0.70 in NYC,
0.50–0.55 in Chicago, 0.37–0.59 in Madrid. The cutoff is now derived from each catalog's own
top-score distribution, landing at **0.450 (Milan) to 0.564 (Madrid)** and yielding worksheets of
**13–16** indicators per city instead of 0 or 69. A z-score was tried first and was wrong twice
over; [the write-up](https://sarapis.github.io/undatacommons-nyc/activity) says why, because the failure is more instructive than the
fix.

**The matcher used to miss what the cities plainly hold — now fixed.** Boston publishes *Vision
Zero Fatality Records*; it ranked 23rd of 235 for "death rate due to road traffic injuries", below
a contract-award file. The cause was document representation, not the query: a static embedding
averaged 60 characters of exactly-right title and tags into 1,500 characters of programme
boilerplate. Scoring title/tags/columns and description as **separate vectors and taking the max**
puts it at **rank 1**, and improves NYC's ground-truth median from **23 to 14** at the same time.

An earlier version of this page said "no substantive SDG indicator has matched outside NYC". That
was true of the matcher and read as a claim about the cities, which was wrong — Chicago publishes
*Traffic Crashes*, *Crimes 2001–Present* and *Open Air Chicago*; Boston publishes *Vision Zero
Fatality Records*. See the [correction](https://sarapis.github.io/undatacommons-nyc/activity).

**Where it stands after the fix.** Boston's worksheet now surfaces *CO₂ emissions → Greenhouse Gas
Emissions* and *Land area → 2016 Land Cover*, alongside survivors like *Food waste → Trash
Schedules by Address*. Roughly half the top candidates are plausible, against two or three in ten
before. Better, and still a worksheet for a person rather than a set of mappings — under
[spec v0.1](https://sarapis.github.io/undatacommons-nyc/spec/) a grade is a human judgment, so the bootstrapper emits
`is_crosswalk: false` by construction.

### Denominators

Rates need a population figure, and a wrong one is invisible in the output. **27 US cities**
resolve via Census ACS; **Madrid** (padrón municipal, 3,520,396) and **Milan** (popolazione
calcolata, an annual series 1880–2025) are wired from their own publications.

Eurostat's Urban Audit is the obvious single source for Europe and is **wrong for this purpose** —
it publishes *greater cities*. Madrid's is 5,115,272 against 3,520,396 for the municipality;
Milan's is 3,580,530 against 1,399,079. Using it would have pushed Milan's rates 60% too low,
silently.

### The portal inventory

The **[municipal table](https://sarapis.github.io/undatacommons-nyc/artifacts/municipal-latest)** covers all **70 municipal portals** with city, country, size, matchable indicators and denominator status; the wider survey reached **372 portals**,
holding **543,000 datasets** between them — 159 Socrata and the rest CKAN.

The primary CKAN source is the **[CKAN Ecosystem Catalog](https://ecosystem.ckan.org)** (NSF POSE
II, 2025): 199 instances, 97 local or regional government. We previously reported that no global
registry existed — that was **wrong**, and we found only its dead predecessors. The abandoned OKFN
list really has rotted (39 of 631 answer), which is what misled us.

One caveat the inventory now states plainly: a portal that does not answer an anonymous
`package_search` is **not** thereby dead. `data.gov` and `govdata.de` refuse the probe and are
obviously alive.

## Data quality — a smell test on the graph

**[UN graph smell test](https://sarapis.github.io/undatacommons-nyc/artifacts/smell-latest)** —
plausibility checks over the **whole corpus: 689 indicators, 773,335 observations**, every
reporting country and year. Malaysia's 147.7% recycling rate was found by accident; this is the
systematic version. **2,503 findings, 93 HIGH.** Five verified errors so far:

| Indicator | What it says | Why it is wrong |
|---|---|---|
| Feel safe walking alone after dark (16.1.4) | Kyrgyzstan **6,710–6,990%**, 2021–23 | Every other observation is 22.8–95.0. ÷100 continues its own trend exactly |
| Municipal waste recycled | South Africa **1.86bn tonnes** | ~90% of all municipal waste on Earth; its own prior years are ~5×10⁵ |
| Hazardous waste per capita | Brunei **12,580 tonnes per person** | Global median 22 **kg**; looks like a national total in a per-capita field |
| E-waste, **four** indicators | Guadeloupe ×1,000 in 2022 | 13.71→13,950 kg/capita and 5,472→5,367,000 t, collected *and* recycled. Makes a territory of 380,000 the world's largest e-waste recycler, 6× the previous maximum |
| Average remittance cost | Malawi **−0.1%, −0.93%** | A cost, negative for two years between normal values |

And one that is **not** an error and matters more: the **United States recorded 345,600 disaster
deaths in 2020 and 470,600 in 2021** — COVID-19, classified as a disaster and reported under
`VC_DSR_MORT`, where every other country's median is 42. Two numbers sharing a variable, a unit
and an axis that are not the same measurement. That is the case for the comparability grade,
made by a check that knows nothing about disasters.

Sweeping all 689 rather than the 442 screened usable added only **5,056 observations (0.65%)**,
and **207 of the extra 247 indicators returned no country data at all** — which retroactively
validates `screen.py`'s six-country panel, whose grade could not in principle distinguish "the
panel does not report this" from "nobody does". It distinguishes them 84% of the time, so **442
remains the right denominator** downstream.

Five of these are written up for the platform team with full evidence, mechanism and suggested
correction: **[data quality report](https://sarapis.github.io/undatacommons-nyc/findings/2026-09-16-data-quality-report)**.

The report also publishes what it **suppressed** (165 groups, 38,943 would-be findings) and what
it cannot reach (123 indicators whose units have no meaningful range). The `Percent` unit in the
graph covers both bounded proportions and signed growth rates, with nothing in the unit string to
tell them apart — which is why an indicator has to be judged against its own distribution rather
than against what its unit is supposed to mean.

## The inverse crosswalk

**[What cities measure that the SDGs do not](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-latest)** —
11,206 datasets from 37 city portals, each matched to its nearest neighbour among all 689 SDG
indicators. Everything else here runs city → UN, which can only find what the framework already
asks about; this runs it backwards.

Themes recurring across many independent catalogs and sitting in the bottom quartile of every one:
**building permits and code enforcement (23 cities)**, **records-access request logs (15)**, bike
and active-travel space (13), street sweeping and parking enforcement (10), **call-centre response
performance (10)**, pedestrian and bicycle counts (9), property sales (8), for-hire vehicle trips
(7), fire stations (7), special events (6).

The sharpest is records access. Fifteen cities publish request logs — filed, answered, how long it
took. The nearest SDG indicator is 16.10.2, *"countries that adopt and implement … guarantees for
public access to information"*: the framework asks whether a **law exists**, the cities publish
whether the law **works**. A country can score full marks and answer nothing.

Going the other way, **123 of 689 indicators were nearest to no municipal dataset at all**. Many
are honestly national (ODA, external debt). But the list also holds **e-waste and hazardous waste
per capita** — the same indicators the US does not report, which cities do not publish either.

Stated plainly: **one positive control in seven failed** (NYC's *Housing Maintenance Code
Violations*, a verified 11.1.1 match, landed at the 24th percentile), and **14 of 40 clusters are
published as diffuse rather than read as themes**. The unit of evidence is cities, not datasets,
precisely because of that.

## The spec

**[City ↔ UN Comparability Spec v0.1](https://sarapis.github.io/undatacommons-nyc/spec/)** — the
grade and tier vocabulary, five rules, a JSON Schema and a validator. Written so another VLR city
can record these judgments in a form a tool can read. `python3 probe/validate_crosswalk.py` checks
this repo's own crosswalk against it.

## The deadline

**Builders' Day — Tue 22 Sep 2026, 10:00–18:00, Google NY (HUD315).** UN Data Commons goes
fully public **17 Sep**. We build against the pre-launch deployment; as of 16 Sep it is unchanged
and the [launch diff](https://sarapis.github.io/undatacommons-nyc/artifacts/launch-diff-latest) is
baselined against it.

| When | What |
|---|---|
| 10:00–12:30 | **Everyone demos.** 5–15 min, single track — everyone sees everything. |
| 14:00–16:00 | Facilitated groups: **evidence provenance · agent tooling on SDMX · trust & QA gates** |
| 16:00–18:00 | **Public showcase** to senior UN managers, during UNGA week |

~40 builders: Google Data Commons engineers, UN innovation staff, NY tech-for-good and
academic teams. The brief is explicit — *bring something you built, and show what surprised you.*

The afternoon themes are almost exactly what this project has been doing: provenance on every
number, and a QA gate that a human judgment can veto.

> **If you are an AI assistant:** this page is the project's shared memory. Read it in full
> before answering questions about the project. It is current as of the date above — check the
> repo's recent commits if that date looks stale. Deeper material is linked at the bottom with
> full URLs you can fetch. For *what happened when*, fetch the
> [activity feed](https://sarapis.github.io/undatacommons-nyc/activity).

**This page is current state and gets overwritten. The
[activity feed](https://sarapis.github.io/undatacommons-nyc/activity) is append-only history.** Read this to know what is true now;
read the feed to know how it got that way.

## What we are building

A **live Voluntary Local Review workbench** for NYC government staff.

New York City published the world's first Voluntary Local Review of the SDGs in 2018. It is a
PDF, produced every few years, by a small team. Meanwhile NYC Open Data and the Mayor's
Management Report publish the same underlying indicators continuously, and the UN System Data
Commons now holds the authoritative global series for the same concepts. Nobody has connected
the two for the person who actually needs it: the analyst at DOT, DOHMH, HPD or OMB writing a
budget justification, a council testimony, or a program review.

Three layers:

1. **An open indicator crosswalk** — NYC Open Data / MMR series mapped to UN indicator DCIDs,
   every mapping carrying a *comparability grade* (direct match / documented proxy / context
   only) and a written reason.
2. **Benchmark views** — NYC's series against the SDG target, the US national series, and peer
   comparators, with definitional caveats on the face of the chart rather than in a footnote.
3. **A natural-language agent** that answers a staffer's question by routing to real queries and
   returning a citable **benchmark card**: number, source, vintage, method, caveat.

## What we have verified about the platform

These are probe results against the live deployment, not documentation claims. Full detail and
reproducible commands: [platform probe findings](https://sarapis.github.io/undatacommons-nyc/findings/2026-09-14-platform-probe).

**1. The graph is national-level. NYC has no UN data.** NYC resolves as an entity
(`geoId/3651000`, type City) but appears in *no* variable's `placesWithData`. Scope a search
to NYC alone and you get zero variables — even for "total population". There is no "look up NYC
in UN Data Commons". **The crosswalk is therefore the product, not a feature of it.**

**2. MCP is governed; REST is federated.** Every variable returned by the MCP tools is
`undata/`-prefixed. The REST endpoint answers for *other publishers'* variables without
warning, so it can hand back a non-UN number that is structurally identical to a UN one.
**Rule: discover through MCP; use REST only for structural walks from an `undata/` id.**

**3. Series density varies wildly, and it will kill a naive demo.** SDG 3.6.1 (road traffic
deaths) returns **one** observation for the US, in 2021. UNICEF population returns 26 annual
points. This is why the coverage probe exists.

**4. Provenance is first-class and machine-readable.** Every observation carries
`provenanceUrl`, `observationPeriod`, `sourceId` and a unit DCID that encodes the
denominator. That makes part of the comparability check automatic rather than hand-curated.

### Where the demo indicators actually are

From the [latest coverage report](https://sarapis.github.io/undatacommons-nyc/artifacts/coverage-latest) — 36 GREEN, 11 AMBER, 9 RED,
re-run 16 Sep. It read 30/9/5 on 14 Sep; the mix moved because `search_indicators` began returning
**more** candidates for the same queries (44 → 56 across nine of fifteen topics, none lost), not
because any indicator changed. Every row present on both dates is identical in all fifteen fields:

| Strong candidates | Why |
|---|---|
| **Homicide rate** (16.1.1) | 21–31 annual points back to 1990; NYC has excellent matching data |
| **Municipal waste recycled** (11.6.1) | 19 points 2000–2018; pairs with DSNY diversion rate |
| **PM2.5** (11.6.2) | 10 points; **and it has a `URBANIZATION--DOU_CITY` slice** |
| **Renewable energy share** (7.2.1) | 34 points 1990–2023 |
| **Unemployment** (8.5.2) | ILO series, dense, sub-annual |

The PM2.5 finding is the interesting one: there is no NYC, but there *is* a "city degree of
urbanization" slice. That is the closest the UN data comes to a city-level comparator, and it
appears across several variables. Worth exploring — it may let us say "NYC vs US cities as a
class" honestly.

**Road safety is out as our headline demo.** It was the example in our application. One data
point cannot carry it.

## The corpus, and how much of it we have touched

**689 base SDG indicators** in the goal framework. Screened against a six-country panel: **442
usable**, of which **130 are indicators the United States does not report** and **67 of those are
city-scoped** — mostly municipal and hazardous waste, wastewater and groundwater. A city can be
compared internationally on exactly the indicators its own country skips. The 11 hand-built pairs are 1.6% of the corpus and 4% of the usable pool — so
the crosswalk is a verified sample, not a representative one.

The `probe/` pipeline now enumerates, screens and proposes candidates from the corpus rather
than from intuition. Its matching stage uses embedding search over the full 2,400-dataset NYC catalog: on seven
hand-verified pairs it puts the correct dataset at median rank **23**, against **1535** for the
keyword matcher it replaced. Still a shortlist for human review, never mappings — about 30% of
real mappings depend on what is *inside* a dataset (NYC's homicide series is offence code 101
inside "NYPD Complaint Data Historic") and no text method can find those.

## What the crosswalk says so far

12 indicator pairs mapped by hand. **Three share an axis as trends** (PM2.5, homicide, waste
recycling), **one ranks but cannot track** (road deaths), and **one has no comparator at all**
(municipal waste — the US reports it to nobody). The remaining seven fail for reasons worth
knowing: mismatched age bands, denominators in a different dataset, concepts that share a name and
measure nothing alike, ceiling effects, and one Tier 1 indicator with no NYC source.

Recording *why* is the product — a crosswalk showing only the easy pairs would be the thing we are
building against.

**Two corrections we made to ourselves, both worth repeating:**

- **Road deaths is not blocked.** We graded it BLOCKED because the UN holds one observation. That
  blocks a *trend* and not a *ranking*: 195 countries reported in 2021, and NYC places **18th of
  196** at 3.51 per 100k — beside Spain and the Netherlands, four times safer than the US. The
  blocker was our framing.
- **The caveat can run either way.** DSNY's residential-only coverage makes NYC look *worse* on
  recycling and *better* on waste per capita. One definitional gap, two opposite distortions.

## Open questions

- **Peer comparators are tiered, not general.** The `URBANIZATION--DOU_CITY` slice lets us
  compare NYC to the **city aggregate of other nations** — same source, method and unit — but a
  scan of 5,320 variables found it on only **five indicators** (PM2.5, built-up area per capita,
  population, two food-insecurity measures). They cluster in gridded-geospatial families; the
  administrative indicators have no spatial dimension and will not gain one. About eight more
  carry a coarser urban/rural cut of little NYC relevance. **The general case remains
  NYC-vs-nation**, so the comparability grade carries most of the weight. See the
  [activity feed](https://sarapis.github.io/undatacommons-nyc/activity).
- **Denominators are solved.** Census ACS 1-year supplies annual NYC population, so
  count-vs-rate pairs work. Requires a free api.census.gov key in `CENSUS_API_KEY` — never
  committed; this repo is public. **Known hole: no ACS 1-year release for 2020**, so 2020
  carries no rate, on the year NYC homicides spiked. Left empty, not interpolated.
- **Will staging DCIDs survive the launch? As of 16 Sep, nothing has moved.** Re-ran every probe
  against the live deployment and diffed it against 14 Sep: 689 base indicators and 6,025 variant
  DCIDs identical, all 689 screened indicators identical in every field, all 57 crosswalk series
  identical value by value, all 12 crosswalk variables identical, demo figures 8/8. The *search
  surface* did move — see the coverage note above — which is the argument for hardcoding
  human-resolved DCIDs rather than searching at runtime.
  [`probe/launch_diff.py`](https://github.com/sarapis/undatacommons-nyc/blob/main/probe/launch_diff.py)
  makes the post-launch re-check one command, and
  [today's diff](https://sarapis.github.io/undatacommons-nyc/artifacts/launch-diff-latest) is the
  pre-launch baseline.
- **For the organizers:** is city-level ingestion on the roadmap? Is there a sanctioned path for
  a city to *contribute* a series? Are there rate limits? And **which host does the public
  deployment answer on** — as of 16 Sep no public hostname resolves, and we are still pointed at
  the deployment we have always used.

## Next steps

- [x] Coverage probe harness — built, run, [results published](https://sarapis.github.io/undatacommons-nyc/artifacts/coverage-latest)
- [x] Pair probe — both sides of every mapping verified,
  [crosswalk status](https://sarapis.github.io/undatacommons-nyc/artifacts/crosswalk-latest)
- [ ] Confirm the peer-comparator framing (recommendation above)
- [x] Census denominators — all three pairs now chartable end to end
- [x] Crosswalk at 12 pairs — 5 on the demo, 7 documented as not comparable and why
  ([status](https://sarapis.github.io/undatacommons-nyc/artifacts/crosswalk-latest))
- [x] Systematic enumeration pipeline — 689 SDG indicators enumerated from the goal trees
  ([candidates](https://sarapis.github.io/undatacommons-nyc/artifacts/candidates-latest))
- [x] Embedding search — correct dataset from median rank 1535 to 23 of 2,400
  ([candidates](https://sarapis.github.io/undatacommons-nyc/artifacts/candidates-latest))
- [x] Screening re-keyed onto a 6-country coverage panel — 442 usable, 130 the US never reports
- [x] City-scope filter replaced with a measured classifier (precision 0.69 → 0.83, recall 1.00)
- [x] Demo at five cards — three trends, one rank-only, one with no comparator
- [x] Multi-city bootstrapping over Socrata + CKAN — plumbing works, matcher does not transfer
- [x] Portal inventory: 372 surveyed, 70 municipal, 543k datasets — CKAN Ecosystem Catalog adopted
- [x] Multilingual embedding model, selected per catalog language (Madrid 0→19, Milan 0→5)
- [x] Per-catalog threshold calibration — cutoff derived from each catalog's own score distribution
- [ ] **17 Sep: re-run every probe against the public launch and diff the DCIDs**
- [ ] Comparability grader using unit DCID + observationPeriod as machine-checkable inputs
- [x] **MCP server** composing UN DC with NYC Open Data — `mcp/server.py`, refuses on
  incomparable pairs and says why ([README](https://github.com/sarapis/undatacommons-nyc/tree/main/mcp))
- [x] Crosswalk shipped as a `SKILL.md` MCP resource, mirroring the platform's own convention

## Map

| What | Where |
|---|---|
| Demo — Eleven Pairs, Three Charts | [https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html](https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html) |
| Activity feed (append-only updates) | [https://sarapis.github.io/undatacommons-nyc/activity](https://sarapis.github.io/undatacommons-nyc/activity) |
| Crosswalk status (both sides verified) | [https://sarapis.github.io/undatacommons-nyc/artifacts/crosswalk-latest](https://sarapis.github.io/undatacommons-nyc/artifacts/crosswalk-latest) |
| Platform probe findings | [https://sarapis.github.io/undatacommons-nyc/findings/2026-09-14-platform-probe](https://sarapis.github.io/undatacommons-nyc/findings/2026-09-14-platform-probe) |
| Latest coverage report | [https://sarapis.github.io/undatacommons-nyc/artifacts/coverage-latest](https://sarapis.github.io/undatacommons-nyc/artifacts/coverage-latest) |
| Launch diff (every DCID the crosswalk expects) | [https://sarapis.github.io/undatacommons-nyc/artifacts/launch-diff-latest](https://sarapis.github.io/undatacommons-nyc/artifacts/launch-diff-latest) |
| UN graph smell test (data-quality sweep) | [https://sarapis.github.io/undatacommons-nyc/artifacts/smell-latest](https://sarapis.github.io/undatacommons-nyc/artifacts/smell-latest) |
| **Data quality report for the platform team** | [https://sarapis.github.io/undatacommons-nyc/findings/2026-09-16-data-quality-report](https://sarapis.github.io/undatacommons-nyc/findings/2026-09-16-data-quality-report) |
| Decision log | [https://sarapis.github.io/undatacommons-nyc/decisions](https://sarapis.github.io/undatacommons-nyc/decisions) |
| Probe harness source | <https://github.com/sarapis/undatacommons-nyc/tree/main/probe> |
| Machine index | [https://sarapis.github.io/undatacommons-nyc/llms.txt](https://sarapis.github.io/undatacommons-nyc/llms.txt) |

## Platform reference

- MCP endpoint: `https://unsd-datacommons.gcp.un-icc.cloud/mcp` — no auth, stateless HTTP.
  Override with `UNDC_ENDPOINT` if the public deployment answers elsewhere.
- REST node endpoint: `https://unsd-datacommons.gcp.un-icc.cloud/core/api/v2/node` (`UNDC_REST`)
- Staging site: <https://staging.undatacommons.unicc.biz/> · public launch 17 Sep 2026.
  No public hostname resolved as of 16 Sep — `undatacommons.unicc.biz` and `datacommons.un.org`
  both refuse to connect.
- Integration guide: <https://projects.officialstatistics.org/undata2/undatacommons-mcp/>
