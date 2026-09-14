---
layout: default
title: Crosswalk candidates — 2026-09-14
---

# Crosswalk candidates — 2026-09-14

Every SDG indicator with a usable US series (248 of 689), searched against the NYC Open Data catalog.

73 were excluded before searching as inherently national (balance of payments, ODA, treaties, fisheries and similar) — a city does not publish them and matching could only yield false positives.

**This is a shortlist for human review, not a set of mappings.** The score is term overlap — good for surfacing a candidate, useless for deciding comparability. Promoting a row into `probe/crosswalk.json` means writing the grade and the reason by hand.

- 248 indicators screened GREEN on the UN side
- 43 have at least one plausible NYC dataset
- **39 are not yet in the crosswalk**

| Score | SDG indicator | UN obs | Candidate NYC dataset | Updated |
|---|---|---:|---|---|
| 1.0 | Municipal waste recycled (`EN_MWT_RCYV`) | 19 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 1.0 | Rate of return on assets (`FI_FSI_FSERA`) | 16 | The Five-System Asset Allocation Chart (`rh3d-kgz3`) | 2026-08-31 |
| 1.0 | Number of local governments (`SG_GOV_LOGV`) | 7 | EEO-4 Reports (`dbpt-pbmd`) | 2024-05-22 |
| 1.0 | Land area (`AG_LND_TOTL`) | 6 | NYC Urban Tree Canopy Assessment Metrics 201 (`hnxz-kkn5`) | 2022-05-09 |
| 0.8 | Proportion of total government spending on essential servi (`SG_XPD_EDUC`) | 24 | IBO Federal Stimulus Budget and Spending Tra (`sg72-pis5`) | 2023-10-05 |
| 0.8 | Minimum reservoir water area as a proportion of total land (`EN_RSRV_MNWAP`) | 23 | Landcover Raster Data (2010) – 3ft Resolutio (`9auy-76zt`) | 2022-05-09 |
| 0.767 | Proportion of people with secure tenure rights to land out (`SP_LGL_LNDSTR`) | 7 | 2021 City Council - September Attendance Rep (`6ucq-tfej`) | 2024-11-26 |
| 0.7 | Carbon dioxide emissions from fuel combustion (`EN_ATM_CO2`) | 24 | NYC Climate Budgeting Report: Emission Facto (`umve-k9rk`) | 2026-05-15 |
| 0.7 | Proportion of population using basic drinking water servic (`SP_ACS_BSRVH2O`) | 20 | Self-Reported Drinking Water Tank Inspection (`gjm4-k24g`) | 2026-09-14 |
| 0.7 | Ratio of liquid assets to short term liabilities (`FI_FSI_FSLS`) | 16 | The Five-System Asset Allocation Chart (`rh3d-kgz3`) | 2026-08-31 |
| 0.667 | Energy intensity level of primary energy (`EG_EGY_PRIM`) | 34 | NYC Municipal Building Energy Benchmarking R (`hpid-63r5`) | 2022-05-09 |
| 0.6 | Share of renewable energy in the total final energy consum (`EG_FEC_RNEW`) | 34 | Local Law 84 Monthly Data (Calendar Year) (`fvp3-gcb2`) | 2025-11-25 |
| 0.6 | Domestic material consumption per capita (`EN_MAT_DOMCMPC`) | 25 | Mayor's Office to End Domestic and Gender-Ba (`mpbx-6c9k`) | 2026-02-24 |
| 0.6 | Annual growth of the gross capital formation (`NE_GDI_TOTL_KD_ZG`) | 25 | Capital Projects Dashboard - Citywide Budget (`fb86-vt7u`) | 2026-07-15 |
| 0.6 | Proportion of population using basic sanitation services (`SP_ACS_BSRVSAN`) | 25 | DSNY Monthly Tonnage Data (`ebb7-mvp5`) | 2026-09-10 |
| 0.6 | Level of water stress: freshwater withdrawal as a proporti (`ER_H2O_STRESS`) | 24 | NYC Wetlands (`p48c-iqtu`) | 2026-01-06 |
| 0.6 | Proportion of total government spending on essential servi (`SG_XPD_ESSRV`) | 24 | Agency Spending by Budget Function (`gzfs-3h4m`) | 2026-07-08 |
| 0.6 | Proportion of total government spending on essential servi (`SG_XPD_HLTH`) | 24 | IBO Federal Stimulus Budget and Spending Tra (`sg72-pis5`) | 2023-10-05 |
| 0.6 | Change in minimum reservoir water area (`EN_RSRV_MNWAC`) | 23 | Landcover Raster Data (2010) – 3ft Resolutio (`9auy-76zt`) | 2022-05-09 |
| 0.6 | Minimum reservoir water area (`EN_RSRV_MNWAN`) | 23 | Watershed Water Quality - Limnology (`3y4p-uusw`) | 2025-05-02 |
| 0.6 | Maxiumum reservoir water area (`EN_RSRV_MXWAN`) | 23 | Watershed Water Quality - Limnology (`3y4p-uusw`) | 2025-05-02 |
| 0.6 | Number of full-time-equivalent researchers per million inh (`GB_POP_SCIERD`) | 23 | Full-Time And Full-Time Equivalent Staffing  (`2t2c-qih9`) | 2026-07-08 |
| 0.6 | Chlorophyll-a deviations, remote sensing (`EN_MAR_CHLDEV`) | 18 | NYC Wetlands Map (`7piy-bhr9`) | 2025-12-06 |
| 0.6 | Detected victims of human trafficking (`VC_HTF_DETV`) | 16 | Mayor's Office to End Domestic and Gender-Ba (`augs-s4dd`) | 2025-06-04 |
| 0.6 | Detected victims of human trafficking for sexual exploitat (`VC_HTF_DETVSX`) | 14 | Mayor's Office to End Domestic and Gender-Ba (`augs-s4dd`) | 2025-06-04 |
| 0.6 | Detected victims of human trafficking for other purposes (`VC_HTF_DETVOP`) | 13 | Mayor's Office to End Domestic and Gender-Ba (`augs-s4dd`) | 2025-06-04 |
| 0.6 | Police reporting rate for sexual assault in the previous 1 (`VC_PRR_SEXV`) | 13 | Family Violence Related Snapshots: New York  (`a35y-93e7`) | 2024-01-31 |
| 0.6 | Electronic waste collected per capita (`EN_EWT_COLLPCAP`) | 11 | Trade Waste Hauler Licensees (`867j-5pgi`) | 2026-09-11 |
| 0.6 | Police reporting rate for physical assault in the previous (`VC_PRR_PHYV`) | 11 | Rates of Intimate Partner Violence Across Ne (`sw27-mp7d`) | 2024-01-31 |
| 0.6 | Police reporting rate for sexual violence in the previous  (`VC_PRR_SEX_VIO`) | 11 | Family Violence Related Snapshots: New York  (`a35y-93e7`) | 2024-01-31 |
| 0.6 | Hazardous waste generated, per capita (`EN_HAZ_PCAP`) | 7 | Self Hauler Registrants (`a8wp-rerh`) | 2026-09-11 |
| 0.6 | Electronic waste generated per capita (`EN_EWT_GENPCAP`) | 6 | Self Hauler Registrants (`a8wp-rerh`) | 2026-09-11 |
| 0.571 | Proportion of total government spending on essential servi (`SD_XPD_ESED`) | 7 | IBO Federal Stimulus Budget and Spending Tra (`sg72-pis5`) | 2023-10-05 |
| 0.5 | Proportion of total government spending on essential servi (`SG_XPD_PROT`) | 24 | IBO Federal Stimulus Budget and Spending Tra (`sg72-pis5`) | 2023-10-05 |
| 0.5 | Permanent water area of lakes and rivers as a proportion o (`EN_LKRV_PWAP`) | 23 | NYC Urban Tree Canopy Assessment Metrics 201 (`hnxz-kkn5`) | 2022-05-09 |
| 0.5 | Seasonal water area of lakes and rivers as a proportion of (`EN_LKRV_SWAP`) | 23 | NYC Urban Tree Canopy Assessment Metrics 201 (`hnxz-kkn5`) | 2022-05-09 |
| 0.5 | Proportion of population covered by at least a 2G mobile n (`IT_MOB_2GNTWK`) | 23 | LinkNYC Usage Statistics (Historical Data) (`69wu-b929`) | 2022-09-23 |
| 0.5 | Proportion of population covered by at least a 3G mobile n (`IT_MOB_3GNTWK`) | 17 | LinkNYC Usage Statistics (Historical Data) (`69wu-b929`) | 2022-09-23 |
| 0.5 | Proportion of population covered by at least a 4G mobile n (`IT_MOB_4GNTWK`) | 13 | LinkNYC Usage Statistics (Historical Data) (`69wu-b929`) | 2022-09-23 |

*Showing the top 60 of 39 unmapped candidates. Regenerate with `python3 probe/match_nyc.py`.*
