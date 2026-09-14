---
layout: default
nav_id: summary
title: Project briefing
---

# UN Data Commons × NYC — project briefing

**Last updated: 2026-09-14** · Team: Devin, Henry, Olivia · [Repo](https://github.com/sarapis/undatacommons-nyc)

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

## Open questions

- **Peer cities.** We told the organizers we would compare NYC to London and Bogotá. UN Data
  Commons alone cannot do that. Either source peer-city data elsewhere (OECD metro, Eurostat
  Urban Audit, UN-Habitat) or reframe as NYC-vs-nations. **Undecided — product call.**
- **For the organizers:** is city-level ingestion on the roadmap? Is there a sanctioned path for
  a city to *contribute* a series? Will staging DCIDs survive the 17 Sep public launch? Are
  there rate limits?

## Next steps

- [x] Coverage probe harness — built, run, [results published](https://sarapis.github.io/undatacommons-nyc/artifacts/coverage-latest)
- [ ] Decide the peer-comparator framing (blocks the benchmark view design)
- [ ] Crosswalk v0, restricted to GREEN indicators, seeded from the 2018 VLR and the MMR
- [ ] Comparability grader using unit DCID + observationPeriod as machine-checkable inputs
- [ ] Bridge service composing UN DC MCP with NYC Open Data
- [ ] Ship our crosswalk as a `SKILL.md` MCP resource, mirroring the platform's own convention

## Map

| What | Where |
|---|---|
| Activity feed (append-only updates) | [https://sarapis.github.io/undatacommons-nyc/activity](https://sarapis.github.io/undatacommons-nyc/activity) |
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
