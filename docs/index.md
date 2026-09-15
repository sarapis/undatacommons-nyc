---
layout: default
nav_id: summary
title: Project briefing
---

# UN Data Commons × NYC — project briefing

**Last updated: 2026-09-15** · Team: Devin, Henry, Olivia · [Repo](https://github.com/sarapis/undatacommons-nyc)

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

The pipeline now runs against **any city** on Socrata or CKAN
([`cities/`](https://github.com/sarapis/undatacommons-nyc/tree/main/cities)), and the first
five-city run is mostly a **negative result worth having**: the plumbing generalises, the matching
does not. Cross-language matching needed a **multilingual embedding model**, now selected per catalog
language — Madrid went 0 → 19 candidates and Milan 0 → 5, with Milan's largely plausible. That fix
is a trade-off, not an upgrade: on the NYC ground truth the English model ranks the correct dataset
at median **23** and the multilingual one at **81**, so English cities keep the English model. The
**similarity threshold still does not transfer between catalogs**, which is now the main blocker —
roughly 2–3 candidates per English city are plausible and no substantive SDG indicator matched
outside NYC.

There is also **no global registry of city open data portals** — every canonical one has rotted —
so [`portals/`](https://github.com/sarapis/undatacommons-nyc/tree/main/portals) constructs one.
The **[portal inventory](https://sarapis.github.io/undatacommons-nyc/artifacts/portals-latest)**
is the result: **198 portals, all responding, 58 municipal**, holding 150k+ datasets between
them. 159 are Socrata and 39 CKAN — the latter being 6% of the only surviving candidate list,
which measures link rot rather than CKAN's popularity.

## The spec

**[City ↔ UN Comparability Spec v0.1](https://sarapis.github.io/undatacommons-nyc/spec/)** — the
grade and tier vocabulary, five rules, a JSON Schema and a validator. Written so another VLR city
can record these judgments in a form a tool can read. `python3 probe/validate_crosswalk.py` checks
this repo's own crosswalk against it.

## The deadline

**Builders' Day — Tue 22 Sep 2026, 10:00–18:00, Google NY (HUD315).** UN Data Commons goes
fully public **17 Sep**; we are building against staging until then.

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

From the [latest coverage report](https://sarapis.github.io/undatacommons-nyc/artifacts/coverage-latest) — 30 GREEN, 9 AMBER, 5 RED:

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
- **For the organizers:** is city-level ingestion on the roadmap? Is there a sanctioned path for
  a city to *contribute* a series? Will staging DCIDs survive the 17 Sep public launch? Are
  there rate limits?

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
- [x] Portal inventory constructed (159 Socrata, 39 CKAN) — no global registry survives
- [x] Multilingual embedding model, selected per catalog language (Madrid 0→19, Milan 0→5)
- [ ] Per-catalog threshold calibration — an absolute cosine score does not travel
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
| Decision log | [https://sarapis.github.io/undatacommons-nyc/decisions](https://sarapis.github.io/undatacommons-nyc/decisions) |
| Probe harness source | <https://github.com/sarapis/undatacommons-nyc/tree/main/probe> |
| Machine index | [https://sarapis.github.io/undatacommons-nyc/llms.txt](https://sarapis.github.io/undatacommons-nyc/llms.txt) |

## Platform reference

- MCP endpoint: `https://unsd-datacommons.gcp.un-icc.cloud/mcp` — no auth, stateless HTTP
- REST node endpoint: `https://unsd-datacommons.gcp.un-icc.cloud/core/api/v2/node`
- Staging site: <https://staging.undatacommons.unicc.biz/> · public launch 17 Sep 2026
- Integration guide: <https://projects.officialstatistics.org/undata2/undatacommons-mcp/>
