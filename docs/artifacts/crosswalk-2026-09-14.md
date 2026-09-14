---
layout: default
title: Crosswalk status — 2026-09-14
---

# Crosswalk status — 2026-09-14

Both sides of every mapping, verified. The grade in each entry is a **human**
judgment recorded in `probe/crosswalk.json`; this page verifies that the mapping
still resolves and that the units agree.

| Pair | SDG | Grade | Chartable | Overlap | Units | Blockers |
|---|---|---|---|---|---|---|
| Fine particulate matter (PM2.5), annual mean | 11.6.2 | PROXY | yes | 2010–2019 | units agree | — |
| Intentional homicide | 16.1.1 | PROXY | yes | 2006–2023 | units agree | — |
| Proportion of municipal waste recycled | 11.6.1 | PROXY | yes | 2000–2018 | units agree | — |

## Detail

### Fine particulate matter (PM2.5), annual mean (SDG 11.6.2) — **PROXY**

*Units agree (ug/m3) and both are annual means, but the methods differ: NYC's figure comes from NYCCAS ground monitors, the UN's is a population-weighted modelled estimate. Comparable in level, not interchangeable. Chart together with the method difference stated.*

- **UN** `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` — 10 obs, 2010–2019, unit `RATIO_WEIGHT_MICROGR_PER_VOL_M3`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `c3uy-2p5r` Air Quality and Health Impacts — 16 obs, 2009–2024, updated 2026-06-18
- Overlap: 2010–2019 · units agree

### Intentional homicide (SDG 16.1.1) — **PROXY**

*NYPD 'murder & non-negligent manslaughter' tracks the UNODC intentional-homicide definition closely. BLOCKER: NYC side is a count, UN side is a rate per 100,000 -- needs an annual NYC population denominator before the two can share an axis. Pre-2006 rows in this dataset carry junk incident dates (17 murders in 1990) and are excluded. Denominator: Census ACS 1-year total population. There is no ACS 1-year release for 2020, so 2020 carries no rate -- and 2020 is the year NYC homicides jumped. That gap is left empty rather than interpolated.*

- **UN** `undata/sdg/VC_IHR_PSRC` — 21 obs, 2000–2023, unit `RATIO_COUNT_PER_100000_COUNT_POP`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `qgea-i56i` NYPD Complaint Data Historic — 18 obs, 2006–2024, updated 2026-04-28
- **Denominator** Census ACS 1-year B01003_001E, NYC place 51000 / state 36, per 100,000 — no denominator for 2020, 2025, those years carry no rate
- Overlap: 2006–2023 · units agree

### Proportion of municipal waste recycled (SDG 11.6.1) — **PROXY**

*DSNY tonnage covers DSNY-collected residential waste only -- it excludes commercial waste, which the UN municipal-waste definition includes. Derived diversion rate, not a published one; the published Recycling Diversion and Capture Rates dataset has not updated since 2020. The month field is text ('2026 / 08') so the year comes from substring, not date_extract_y. Rows before 1993 predate curbside recycling (no recycling tonnage, 1990 partial) and are excluded.*

- **UN** `undata/sdg/EN_MWT_RCYR` — 19 obs, 2000–2018, unit `Percent`, source https://unstats.un.org/sdgs/dataportal
- **NYC** `ebb7-mvp5` DSNY Monthly Tonnage Data — 34 obs, 1993–2026, updated 2026-09-10
- Overlap: 2000–2018 · units agree
