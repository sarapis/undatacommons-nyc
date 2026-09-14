---
layout: default
title: "Correction: the city-level comparator covers five indicators, not the general case"
author: Devin
date: 2026-09-14 19:00:00 -0400
---

Earlier today I reported that `URBANIZATION--DOU_CITY` recovers peer-city comparison and
recommended it as the primary framing. That was an over-generalisation from the one indicator I
tested it on. Scoping it properly changes the picture.

Scanned 23 topic areas, 5,320 variables. Indicators carrying a `DOU_CITY` slice: **five.**

- `undata/sdg/EN_ATM_PM25` — PM2.5
- `undata/unicef/DM_BU_PC_DOU` — built-up area per capita
- `undata/unicef/DM_POP` — population
- `undata/sdg/AG_PRD_FIESS` / `AG_PRD_FIESMS` — food insecurity

They cluster in indicators derived from **gridded geospatial data** (the GHSL settlement layer),
which is the only family where a national figure can be cut by settlement type. Homicide, waste,
unemployment, poverty and renewable energy have no such dimension and will not get one — they
come from administrative reporting with no spatial component.

About eight more indicators carry only `DOU_U` (urban vs rural). DEGURBA "urban" bundles cities
with towns and suburbs, so it is a coarser class, and the indicators it covers skew toward
electricity access, handwashing and open defecation — little NYC relevance. Slums and school
completion are the exceptions.

## The comparator is tiered, not general

| Tier | Comparator | Coverage |
|---|---|---|
| 1 | NYC vs national **city** aggregates, many countries | ~5 indicators |
| 2 | NYC vs national **urban** aggregates | ~8, mostly low NYC relevance |
| 3 | NYC vs **national totals** | everything else — the large majority |

Tier 1 is real and PM2.5 is an excellent demo of it. The general case is still Tier 3.

That is arguably a better story than "we found city-level UN data." It means the tool's core job
is telling a user **which tier they are in and what that permits them to claim**. A naive
dashboard renders all three tiers as identical bar charts, and that is precisely the failure
we are building against.
