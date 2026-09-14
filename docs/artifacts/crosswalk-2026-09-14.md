---
layout: default
title: Crosswalk status — 2026-09-14
---

# Crosswalk status — 2026-09-14

Both sides of every mapping, verified. The grade in each entry is a **human**
judgment recorded in `probe/crosswalk.json`; this page verifies that the mapping
still resolves and that the units agree.

Tier 1 = NYC vs national **city** aggregates · Tier 2 = urban aggregates · Tier 3 = national totals. The tier says what the comparison is worth.

| Pair | SDG | Tier | Grade | Chartable | Overlap | Blockers |
|---|---|---|---|---|---|---|
| Fine particulate matter (PM2.5), annual mean | 11.6.2 | 1 | PROXY | yes | 2010–2019 | — |
| Intentional homicide | 16.1.1 | 3 | PROXY | yes | 2006–2023 | — |
| Proportion of municipal waste recycled | 11.6.1 | 3 | PROXY | yes | 2000–2018 | — |
| Road traffic deaths | 3.6.1 | 3 | BLOCKED | NO | 2021–2021 | grade BLOCKED: human judgment says these must not share an axis |
| Child mortality (deaths) | 3.2.1 | 3 | CONTEXT | NO | 2021–2023 | grade CONTEXT: human judgment says these must not share an axis |
| Maternal mortality | 3.1.1 | 3 | BLOCKED | NO | 2016–2021 | grade BLOCKED: human judgment says these must not share an axis |
| Deaths attributable to ambient air pollution | 3.9.1 | 3 | CONTEXT | NO | 2012–2017 | grade CONTEXT: human judgment says these must not share an axis |
| Poverty | 1.2.1 | 3 | CONTEXT | NO | — | no NYC counterpart identified |
| Inadequate housing | 11.1.1 | 2 | CONTEXT | NO | 2010–2022 | UNIT MISMATCH: UN `Percent` vs NYC `count`; grade CONTEXT: human judgment says these must not share an axis |
| Built-up area per capita (cities) | 11.7.1 | 1 | NO-NYC-SOURCE | NO | — | no NYC counterpart identified |
| Safely managed drinking water | 6.1.1 | 3 | NO-SIGNAL | NO | — | no NYC counterpart identified |

## Detail

### Fine particulate matter (PM2.5), annual mean (SDG 11.6.2) — **PROXY**, Tier 1

*Units agree (ug/m3) and both are annual means, but the methods differ: NYC's figure comes from NYCCAS ground monitors, the UN's is a population-weighted modelled estimate. Comparable in level, not interchangeable. Chart together with the method difference stated.*

- **UN** `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` — 10 obs, 2010–2019, unit `RATIO_WEIGHT_MICROGR_PER_VOL_M3`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `c3uy-2p5r` Air Quality and Health Impacts — 16 obs, 2009–2024, updated 2026-06-18
- Overlap: 2010–2019 · units agree

### Intentional homicide (SDG 16.1.1) — **PROXY**, Tier 3

*NYPD 'murder & non-negligent manslaughter' tracks the UNODC intentional-homicide definition closely. BLOCKER: NYC side is a count, UN side is a rate per 100,000 -- needs an annual NYC population denominator before the two can share an axis. Pre-2006 rows in this dataset carry junk incident dates (17 murders in 1990) and are excluded. Denominator: Census ACS 1-year total population. There is no ACS 1-year release for 2020, so 2020 carries no rate -- and 2020 is the year NYC homicides jumped. That gap is left empty rather than interpolated.*

- **UN** `undata/sdg/VC_IHR_PSRC` — 21 obs, 2000–2023, unit `RATIO_COUNT_PER_100000_COUNT_POP`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `qgea-i56i` NYPD Complaint Data Historic — 18 obs, 2006–2024, updated 2026-04-28
- **Denominator** Census ACS 1-year B01003_001E, NYC place 51000 / state 36, per 100,000 — no denominator for 2020, 2025, those years carry no rate
- Overlap: 2006–2023 · units agree

### Proportion of municipal waste recycled (SDG 11.6.1) — **PROXY**, Tier 3

*DSNY tonnage covers DSNY-collected residential waste only -- it excludes commercial waste, which the UN municipal-waste definition includes. Derived diversion rate, not a published one; the published Recycling Diversion and Capture Rates dataset has not updated since 2020. The month field is text ('2026 / 08') so the year comes from substring, not date_extract_y. Rows before 1993 predate curbside recycling (no recycling tonnage, 1990 partial) and are excluded.*

- **UN** `undata/sdg/EN_MWT_RCYR` — 19 obs, 2000–2018, unit `Percent`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `ebb7-mvp5` DSNY Monthly Tonnage Data — 34 obs, 1993–2026, updated 2026-09-10
- Overlap: 2000–2018 · units agree

### Road traffic deaths (SDG 3.6.1) — **BLOCKED**, Tier 3

*NYC has an excellent series (Vision Zero collision data, daily updates). The UN side has ONE observation, 2021, a periodic WHO modelled estimate. Kept in the crosswalk deliberately: this is what a blocked pair looks like, and the blocker is the UN side, not ours.*

- **UN** `undata/sdg/SH_STA_TRAF` — 1 obs, 2021–2021, unit `RATIO_COUNT_PER_100000_COUNT_POP`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `h9gi-nx95` Motor Vehicle Collisions - Crashes — 11 obs, 2013–2024, updated 2026-07-31
- **Denominator** Census ACS 1-year B01003_001E, NYC place 51000 / state 36, per 100,000 — no denominator for 2020, 2025, 2026, those years carry no rate
- Overlap: 2021–2021 · units agree

  **Blockers:** grade BLOCKED: human judgment says these must not share an axis

### Child mortality (deaths) (SDG 3.2.1) — **CONTEXT**, Tier 3

*AGE BANDS DO NOT MATCH. The UN counts deaths under five; NYC's infant mortality dataset counts deaths under one. Both are raw counts so the units 'agree', which is exactly the trap -- a chart would look correct and compare different populations. Show side by side, never on one axis, until an under-five NYC series is sourced.*

- **UN** `undata/who/CHILD_DEATHS.AGE--Y0T4` — 69 obs, 1955–2023, unit `COUNT_DEATHS`, source https://www.who.int/data
- **NYC** `fcau-jc6k` Infant Mortality — 3 obs, 2021–2023, updated 2026-04-14
- Overlap: 2021–2023 · unmapped UN unit `COUNT_DEATHS` - check by hand

  **Blockers:** grade CONTEXT: human judgment says these must not share an axis

### Maternal mortality (SDG 3.1.1) — **BLOCKED**, Tier 3

*Two problems. NYC publishes pregnancy-ASSOCIATED deaths (any cause within a year of pregnancy), a deliberately broader definition than the UN's maternal mortality. And the UN rate is per 100,000 LIVE BIRTHS, not per population -- the denominator lives in a different NYC dataset (fcau-jc6k number_of_live_births). Needs a cross-dataset join before it can be charted.*

- **UN** `undata/sdg/SH_STA_MORT.SEX--F` — 24 obs, 2000–2023, unit `RATIO_COUNT_PER_100000_COUNT_LIVEBIRTHS`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `27x4-cbi6` Pregnancy-Associated Mortality — 6 obs, 2016–2021, updated 2025-10-23
- Overlap: 2016–2021 · unmapped UN unit `RATIO_COUNT_PER_100000_COUNT_LIVEBIRTHS` - check by hand

  **Blockers:** grade BLOCKED: human judgment says these must not share an axis

### Deaths attributable to ambient air pollution (SDG 3.9.1) — **CONTEXT**, Tier 3

*UN reports a national death COUNT attributable to ambient air pollution; NYC reports an age-adjusted RATE for ages 30+ attributable to PM2.5 specifically. Different measure, different age base, different pollutant scope. Informative side by side, not comparable on one axis.*

- **UN** `undata/who/AIR_DEATH.AIR_POL_TYPE--AMB` — 10 obs, 2010–2019, unit `COUNT_DEATHS`, source https://www.who.int/data
- **NYC** `c3uy-2p5r` Air Quality and Health Impacts — 5 obs, 2005–2017, updated 2026-06-18
- Overlap: 2012–2017 · unmapped UN unit `COUNT_DEATHS` - check by hand

  **Blockers:** grade CONTEXT: human judgment says these must not share an axis

### Poverty (SDG 1.2.1) — **CONTEXT**, Tier 3

*NOT THE SAME CONCEPT. The UN series is the share below the INTERNATIONAL extreme-poverty line (~$2.15/day PPP), which is near zero for any US city and carries no signal. NYC's own poverty measure is a cost-of-living-adjusted threshold an order of magnitude higher. Also the NYCgov measure is published as a separate dataset per year, so there is no continuous series to query. Included as the clearest example of two numbers that share a name and measure nothing alike.*

- **UN** `undata/sdg/SI_POV_DAY1` — 61 obs, 1963–2023, unit `Percent`, source https://unstats.un.org/sdgs/dataportal
- **NYC** — no counterpart identified
- Overlap: — · n/a — no NYC source

  **Blockers:** no NYC counterpart identified

### Inadequate housing (SDG 11.1.1) — **CONTEXT**, Tier 2

*UN measures the SHARE OF URBAN POPULATION living in slums. NYC's nearest analogue is a COUNT of class C (immediately hazardous) housing maintenance violations -- an enforcement output, not a population share, and sensitive to inspection rates rather than to conditions alone. Directionally interesting, structurally different. Tier 2: the UN side is urban, which bundles cities with suburbs.*

- **UN** `undata/sdg/EN_LND_SLUM.URBANIZATION--DOU_U` — 12 obs, 2000–2022, unit `Percent`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `wvxf-dwi5` Housing Maintenance Code Violations — 17 obs, 2010–2026, updated 2026-09-14
- Overlap: 2010–2022 · UNIT MISMATCH: UN `Percent` vs NYC `count`

  **Blockers:** UNIT MISMATCH: UN `Percent` vs NYC `count`; grade CONTEXT: human judgment says these must not share an axis

### Built-up area per capita (cities) (SDG 11.7.1) — **NO-NYC-SOURCE**, Tier 1

*Tier 1 UN data exists with a full 2000-2025 series and city-level slices across countries, but no NYC Open Data equivalent has been identified. Candidates to investigate: PLUTO lot area aggregates, Parks Properties. Recorded so the gap is visible rather than forgotten.*

- **UN** `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` — 26 obs, 2000–2025, unit `COUNT`, source https://data.unicef.org/
- **NYC** — no counterpart identified
- Overlap: — · n/a — no NYC source

  **Blockers:** no NYC counterpart identified

### Safely managed drinking water (SDG 6.1.1) — **NO-SIGNAL**, Tier 3

*The UN series sits at or near 100% for the US across the whole window, as it would for NYC. A chart of two flat lines at 100 tells a policy analyst nothing. Recorded as deliberately excluded rather than overlooked -- a ceiling effect is a reason not to build a view, and that judgment should be written down.*

- **UN** `undata/sdg/SH_H2O_SAFE` — 20 obs, 2005–2024, unit `Percent`, source https://unstats.un.org/sdgs/dataportal
- **NYC** — no counterpart identified
- Overlap: — · n/a — no NYC source

  **Blockers:** no NYC counterpart identified

## Summary

**11 pairs · 3 chartable end to end.**

- CONTEXT: 4
- PROXY: 3
- BLOCKED: 2
- NO-NYC-SOURCE: 1
- NO-SIGNAL: 1

A blocked or context-only pair is not a failure. Recording *why* two numbers
cannot share an axis is the product; a crosswalk showing only the easy pairs
would be the thing we are building against.
