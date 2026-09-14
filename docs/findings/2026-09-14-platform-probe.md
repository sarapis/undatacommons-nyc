---
layout: default
title: Platform probe findings — 2026-09-14
---

# UN System Data Commons — pre-build technical findings

Probed 2026-09-14 against the live staging deployment. Every result below is reproducible with
`curl` or with `probe/undc.py`.

## Surface

- **MCP endpoint:** `https://unsd-datacommons.gcp.un-icc.cloud/mcp` — live, **no auth**,
  streamable HTTP, answers stateless JSON-RPC. Server `DC MCP Server v1.3.0`, protocol
  `2025-06-18`.
- **6 tools:** `search_indicators`, `search_child_indicators`, `get_variable_metadata`,
  `get_observations`, `get_child_observations`, `get_multi_entity_observations`.
- **3 playbook resources:** `skill://data-commons-researcher/SKILL.md`,
  `skill://data-commons-child-places-researcher/SKILL.md`,
  `skill://data-commons-multi-entity-researcher/SKILL.md`. The server's instructions *mandate*
  reading the relevant playbook before tool calls, mandate per-datapoint attribution, and
  forbid guessing DCIDs.
- **REST:** `https://unsd-datacommons.gcp.un-icc.cloud/core/api/v2/node` — structural walks only.

## Finding 1 — the graph is national-level. NYC has no UN data.

`search_indicators(query="road traffic deaths", places=["New York City","United States"])`:

- NYC **resolves** as an entity: `geoId/3651000`, type `City`.
- Every returned variable lists `placesWithData: ["country/USA"]`. NYC appears in **none**.
- Scoping a search to NYC alone returns **zero variables and zero topics** — even for
  "total population".
- `search_child_indicators(parent="United States", children=[NYC, LA, Chicago])` for PM2.5:
  **empty**.

`places` is a data-availability filter, not a hint. Scope to a city and you get an empty set.

**Implication:** there is no "look up NYC in UN Data Commons". The crosswalk *is* the product.

**Partial exception, worth exploring:** several variables carry an
`URBANIZATION--DOU_CITY` dimension (`undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY`,
`undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY`). That is a national figure sliced by
degree of urbanization — "the city parts of the US" — not a figure for any particular city.
It may still be the most honest available comparator for a NYC number.

## Finding 2 — MCP is governed; REST is federated. Discover via MCP only.

Every variable returned by MCP search is `undata/`-prefixed (`undata/sdg/*`, `undata/who/*`,
`undata/unicef/*`, `undata/ilo/*`, `undata/unodc/*`, `undata/itu/*`, `undata/unido/*`). No
leakage observed across any probe.

The REST guide warns that the same endpoints answer for *other publishers'* variables without
warning — so REST can silently return a non-UN number that is structurally identical to a UN
one. **Rule: discover through MCP; use REST only for structural walks starting from an
`undata/` identifier.**

## Finding 3 — series density varies wildly. This can kill a demo.

Verified with `date:"all"`:

| Variable | n obs | Years |
|---|---:|---|
| `undata/unicef/DM_POP` | 26 | 2000–2024, annual |
| `undata/sdg/SH_STA_TRAF` (SDG 3.6.1) | **1** | 2021 |
| `undata/who/ROAD_DEATH_RATE` | **1** | 2021 |

`date:"all"` works correctly — UNICEF proves it. The sparsity is genuine: WHO road-death figures
are periodic **modelled estimates**, not an annual administrative series. A "NYC trend vs SDG
target" chart on 3.6.1 is not possible from this source.

This finding is what the [coverage probe](https://github.com/sarapis/undatacommons-nyc/tree/main/probe)
exists to systematize.

## Finding 4 — provenance is first-class

Every observation carries `provenanceUrl`, a unit DCID (e.g.
`undata/UNIT_MEASURE-RATIO_COUNT_PER_100000_COUNT_POP`), `observationPeriod` (`P1Y`) and
`sourceId`. Unit and period are machine-readable, so a NYC per-100k rate against a UN per-100k
rate is a checkable match rather than a judgment call. That makes part of our comparability
grader automatic.

## Consequence for the application we submitted

The pitch survives — the bridge is the value, and the platform's own governance boundary gives
our comparability grade a machine-checkable basis. One promise needs revisiting: we said we
would compare NYC to **peer cities** (London, Bogotá). UN Data Commons alone cannot do that.
Either source peer-city data elsewhere (OECD metro, Eurostat Urban Audit, UN-Habitat) or reframe
as NYC-vs-nations.
