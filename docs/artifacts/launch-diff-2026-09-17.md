---
layout: default
title: Launch diff — 2026-09-17
---

# Launch diff — 2026-09-17

Baseline taken 2026-09-16T10:18:47 · this run 2026-09-17T11:44:32.

Endpoint `https://unsd-datacommons.gcp.un-icc.cloud/mcp`.

**No drift.** Every DCID the crosswalk names still resolves to the same series, with the same values.

- 57 series checked · 0 changed · 3 empty · 0 errored
- 12 variables checked · 0 changed
- corpus 689 -> 689 base indicators · 0 added · 0 removed
- tools: ['search_indicators', 'search_child_indicators', 'get_variable_metadata', 'get_observations', 'get_child_observations', 'get_multi_entity_observations']
- REST node endpoint: answering

## Series

Every (variable, place) the crosswalk and its peer comparators depend on. An `EMPTY` status is the dangerous one — a withdrawn DCID and a country that does not report are the same shape.

| Pair | Variable @ place | Status | Verdict | Detail |
|---|---|---|---|---|
| pm25 | `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` @ `country/CAN` | OK | same | identical |
| pm25 | `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` @ `country/FRA` | OK | same | identical |
| pm25 | `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` @ `country/GBR` | OK | same | identical |
| pm25 | `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` @ `country/JPN` | OK | same | identical |
| pm25 | `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` @ `country/MEX` | OK | same | identical |
| pm25 | `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` @ `country/USA` | OK | same | identical |
| housing-inadequate | `undata/sdg/EN_LND_SLUM.URBANIZATION--DOU_U` @ `country/COL` | OK | same | identical |
| housing-inadequate | `undata/sdg/EN_LND_SLUM.URBANIZATION--DOU_U` @ `country/GBR` | OK | same | identical |
| housing-inadequate | `undata/sdg/EN_LND_SLUM.URBANIZATION--DOU_U` @ `country/MEX` | OK | same | identical |
| housing-inadequate | `undata/sdg/EN_LND_SLUM.URBANIZATION--DOU_U` @ `country/USA` | OK | same | identical |
| municipal-waste | `undata/sdg/EN_MWT_COLLV` @ `country/DEU` | OK | same | identical |
| municipal-waste | `undata/sdg/EN_MWT_COLLV` @ `country/FRA` | OK | same | identical |
| municipal-waste | `undata/sdg/EN_MWT_COLLV` @ `country/JPN` | EMPTY | same | EMPTY |
| municipal-waste | `undata/sdg/EN_MWT_COLLV` @ `country/MEX` | EMPTY | same | EMPTY |
| municipal-waste | `undata/sdg/EN_MWT_COLLV` @ `country/USA` | EMPTY | same | EMPTY |
| waste-recycled | `undata/sdg/EN_MWT_RCYR` @ `country/CAN` | OK | same | identical |
| waste-recycled | `undata/sdg/EN_MWT_RCYR` @ `country/FRA` | OK | same | identical |
| waste-recycled | `undata/sdg/EN_MWT_RCYR` @ `country/GBR` | OK | same | identical |
| waste-recycled | `undata/sdg/EN_MWT_RCYR` @ `country/JPN` | OK | same | identical |
| waste-recycled | `undata/sdg/EN_MWT_RCYR` @ `country/USA` | OK | same | identical |
| drinking-water | `undata/sdg/SH_H2O_SAFE` @ `country/COL` | OK | same | identical |
| drinking-water | `undata/sdg/SH_H2O_SAFE` @ `country/GBR` | OK | same | identical |
| drinking-water | `undata/sdg/SH_H2O_SAFE` @ `country/MEX` | OK | same | identical |
| drinking-water | `undata/sdg/SH_H2O_SAFE` @ `country/USA` | OK | same | identical |
| maternal-mortality | `undata/sdg/SH_STA_MORT.SEX--F` @ `country/CAN` | OK | same | identical |
| maternal-mortality | `undata/sdg/SH_STA_MORT.SEX--F` @ `country/FRA` | OK | same | identical |
| maternal-mortality | `undata/sdg/SH_STA_MORT.SEX--F` @ `country/GBR` | OK | same | identical |
| maternal-mortality | `undata/sdg/SH_STA_MORT.SEX--F` @ `country/JPN` | OK | same | identical |
| maternal-mortality | `undata/sdg/SH_STA_MORT.SEX--F` @ `country/USA` | OK | same | identical |
| road-deaths | `undata/sdg/SH_STA_TRAF` @ `country/CAN` | OK | same | identical |
| road-deaths | `undata/sdg/SH_STA_TRAF` @ `country/FRA` | OK | same | identical |
| road-deaths | `undata/sdg/SH_STA_TRAF` @ `country/GBR` | OK | same | identical |
| road-deaths | `undata/sdg/SH_STA_TRAF` @ `country/JPN` | OK | same | identical |
| road-deaths | `undata/sdg/SH_STA_TRAF` @ `country/USA` | OK | same | identical |
| poverty | `undata/sdg/SI_POV_DAY1` @ `country/COL` | OK | same | identical |
| poverty | `undata/sdg/SI_POV_DAY1` @ `country/GBR` | OK | same | identical |
| poverty | `undata/sdg/SI_POV_DAY1` @ `country/MEX` | OK | same | identical |
| poverty | `undata/sdg/SI_POV_DAY1` @ `country/USA` | OK | same | identical |
| homicide | `undata/sdg/VC_IHR_PSRC` @ `country/CAN` | OK | same | identical |
| homicide | `undata/sdg/VC_IHR_PSRC` @ `country/FRA` | OK | same | identical |
| homicide | `undata/sdg/VC_IHR_PSRC` @ `country/GBR` | OK | same | identical |
| homicide | `undata/sdg/VC_IHR_PSRC` @ `country/JPN` | OK | same | identical |
| homicide | `undata/sdg/VC_IHR_PSRC` @ `country/USA` | OK | same | identical |
| built-up-area | `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` @ `country/CAN` | OK | same | identical |
| built-up-area | `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` @ `country/FRA` | OK | same | identical |
| built-up-area | `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` @ `country/GBR` | OK | same | identical |
| built-up-area | `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` @ `country/JPN` | OK | same | identical |
| built-up-area | `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` @ `country/MEX` | OK | same | identical |
| built-up-area | `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` @ `country/USA` | OK | same | identical |
| air-pollution-deaths | `undata/who/AIR_DEATH.AIR_POL_TYPE--AMB` @ `country/FRA` | OK | same | identical |
| air-pollution-deaths | `undata/who/AIR_DEATH.AIR_POL_TYPE--AMB` @ `country/GBR` | OK | same | identical |
| air-pollution-deaths | `undata/who/AIR_DEATH.AIR_POL_TYPE--AMB` @ `country/JPN` | OK | same | identical |
| air-pollution-deaths | `undata/who/AIR_DEATH.AIR_POL_TYPE--AMB` @ `country/USA` | OK | same | identical |
| child-mortality | `undata/who/CHILD_DEATHS.AGE--Y0T4` @ `country/FRA` | OK | same | identical |
| child-mortality | `undata/who/CHILD_DEATHS.AGE--Y0T4` @ `country/GBR` | OK | same | identical |
| child-mortality | `undata/who/CHILD_DEATHS.AGE--Y0T4` @ `country/JPN` | OK | same | identical |
| child-mortality | `undata/who/CHILD_DEATHS.AGE--Y0T4` @ `country/USA` | OK | same | identical |

## Variables

Resolved through `get_variable_metadata`, which catches a rename or a redefinition even where observations still flow.

| DCID | Status | Verdict | Detail |
|---|---|---|---|
| `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` | OK | same | identical |
| `undata/sdg/EN_LND_SLUM.URBANIZATION--DOU_U` | OK | same | identical |
| `undata/sdg/EN_MWT_COLLV` | OK | same | identical |
| `undata/sdg/EN_MWT_RCYR` | OK | same | identical |
| `undata/sdg/SH_H2O_SAFE` | OK | same | identical |
| `undata/sdg/SH_STA_MORT.SEX--F` | OK | same | identical |
| `undata/sdg/SH_STA_TRAF` | OK | same | identical |
| `undata/sdg/SI_POV_DAY1` | OK | same | identical |
| `undata/sdg/VC_IHR_PSRC` | OK | same | identical |
| `undata/unicef/DM_BU_PC_DOU.URBANIZATION--DOU_CITY` | OK | same | identical |
| `undata/who/AIR_DEATH.AIR_POL_TYPE--AMB` | OK | same | identical |
| `undata/who/CHILD_DEATHS.AGE--Y0T4` | OK | same | identical |

## Corpus

SDG base indicators enumerated: **689** at baseline, **689** now.

No indicator appeared or vanished.

