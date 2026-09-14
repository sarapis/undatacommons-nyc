---
layout: default
title: Crosswalk candidates — 2026-09-14
---

# Crosswalk candidates — 2026-09-14

Every SDG indicator with a usable US series (248 of 689), searched against the NYC Open Data catalog.

73 were excluded before searching as inherently national (balance of payments, ODA, treaties, fisheries and similar) — a city does not publish them and matching could only yield false positives.

Retrieval: **embedding**. Embedding search over the full 2,400-dataset catalog (name, description, columns, tags, category), which on our seven verified pairs put the correct dataset at median rank **23** versus **1535** for keyword overlap.

**This is a shortlist for human review, not a set of mappings.** Similarity surfaces a candidate; it cannot decide comparability. Two of those seven verified pairs stay unfindable at any rank because the mapping depends on what is *inside* a dataset — NYC's homicide series is offence code 101 inside 'NYPD Complaint Data Historic', which its metadata never mentions. Promoting a row into `probe/crosswalk.json` means writing the grade and the reason by hand.

- 248 indicators screened GREEN on the UN side
- 53 have at least one NYC dataset above the 0.5 similarity floor
- **50 are not yet in the crosswalk**

| Score | SDG indicator | UN obs | Candidate NYC dataset | Updated |
|---|---|---:|---|---|
| 0.702 | Municipal waste recycled (`EN_MWT_RCYV`) | 19 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.634 | Number of victims of intentional homicide (`VC_IHR_PSRCN`) | 31 | Domestic Violence Homicide Incidents in the  (`u97r-kgca`) | 2024-01-31 |
| 0.627 | Total electronic waste collected (`EN_EWT_COLLV`) | 11 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.617 | Share of renewable energy in the total final energy consum (`EG_FEC_RNEW`) | 34 | Local Law 84 Monthly Data (Calendar Year) (`fvp3-gcb2`) | 2025-11-25 |
| 0.617 | Number of fixed broadband subscriptions (`IT_NET_BBNDN`) | 25 | Broadband Adoption and Infrastructure by Cou (`cgwq-3ie6`) | 2022-09-23 |
| 0.61 | Proportion of domestic budget funded by domestic taxes (`GC_GOB_TAXD`) | 24 | Expense Budget--Miscellaneous Expense by Cat (`fdgu-y9iy`) | 2026-07-08 |
| 0.609 | Fixed broadband subscriptions per 100 inhabitants (`IT_NET_BBND`) | 25 | Broadband Adoption and Infrastructure by Cou (`cgwq-3ie6`) | 2022-09-23 |
| 0.607 | Police reporting rate for sexual violence in the previous  (`VC_PRR_SEX_VIO`) | 11 | ENDGBV: The Intersection of Domestic Violenc (`2rb7-7eqa`) | 2024-01-31 |
| 0.606 | Police reporting rate for sexual assault in the previous 1 (`VC_PRR_SEXV`) | 13 | ENDGBV: The Intersection of Domestic Violenc (`2rb7-7eqa`) | 2024-01-31 |
| 0.59 | Performance index of data Infrastructure (Pillar 5 of Stat (`IQ_SPI_PIL5`) | 8 | PMMR Performance Indicators FY2013-15 (Histo (`n6uf-ruxa`) | 2023-11-30 |
| 0.585 | Proportion of total government spending on essential servi (`SG_XPD_EDUC`) | 24 | CBO Expense Report (`rdjw-z878`) | 2020-04-25 |
| 0.585 | Proportion of total government spending on essential servi (`SG_XPD_ESSRV`) | 24 | CBO Expense Report (`rdjw-z878`) | 2020-04-25 |
| 0.584 | Annual growth of final consumption expenditure of the gene (`NE_CON_GOVT_KD_ZG`) | 23 | Mayor's Management Report Spending and Budge (`2jrp-puwz`) | 2025-09-24 |
| 0.578 | Performance index of data sources (Pillar 4 of Statistical (`IQ_SPI_PIL4`) | 8 | PMMR Performance Indicators FY2013-15 (Histo (`n6uf-ruxa`) | 2023-11-30 |
| 0.563 | Police reporting rate for robbery in the previous 12 month (`VC_PRR_ROBB`) | 17 | DOP Adult Probationers Rearrested As A Perce (`arhf-esqb`) | 2026-08-04 |
| 0.558 | Minimum reservoir water area as a proportion of total land (`EN_RSRV_MNWAP`) | 23 | Census Demographics at the Neighborhood Tabu (`rnsn-acs2`) | 2020-02-08 |
| 0.556 | Installed renewable electricity-generating capacity (`EG_EGY_RNEW`) | 25 | City of New York Municipal Solar-Readiness A (`cfz5-6fvh`) | 2026-04-16 |
| 0.554 | Proportion of total government spending on essential servi (`SG_XPD_HLTH`) | 24 | CBO Expense Report (`rdjw-z878`) | 2020-04-25 |
| 0.553 | Electronic waste collected per capita (`EN_EWT_COLLPCAP`) | 11 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.551 | Carbon dioxide emissions from fuel combustion (`EN_ATM_CO2`) | 24 | Office of Climate and Sustainability: 2019 F (`psr5-vz6y`) | 2024-01-24 |
| 0.551 | Police reporting rate for physical assault in the previous (`VC_PRR_PHYV`) | 11 | ENDGBV: The Intersection of Domestic Violenc (`2rb7-7eqa`) | 2024-01-31 |
| 0.549 | Proportion of the population with positive out-of-pocket h (`SH_OOP_XPD_EARNNET40`) | 24 | NYCHA Resident Data Book Summary (`5r5y-pvs3`) | 2025-08-01 |
| 0.549 | Suicide mortality rate (`SH_STA_SCIDE`) | 7 | New York City Leading Causes of Death (`jb7j-dtam`) | 2026-01-27 |
| 0.548 | Number of deaths due to disaster (`VC_DSR_MORT`) | 7 | New York City Leading Causes of Death (`jb7j-dtam`) | 2026-01-27 |
| 0.548 | Total electronic waste generated (`EN_EWT_GENV`) | 6 | DSNY Waste Characterization - Comparative Re (`bibp-6ff7`) | 2024-05-02 |
| 0.544 | Land area (`AG_LND_TOTL`) | 6 | Functional Parkland (`xhvt-s4va`) | 2026-08-16 |
| 0.543 | Number of full-time-equivalent researchers per million inh (`GB_POP_SCIERD`) | 23 | Full-Time And Full-Time Equivalent Staffing  (`2t2c-qih9`) | 2026-07-08 |
| 0.541 | Domestic material consumption per capita (`EN_MAT_DOMCMPC`) | 25 | Water Consumption in the City of New York (`ia2d-e54m`) | 2025-05-21 |
| 0.539 | Proportion of local governments that adopt and implement l (`SG_DSR_SILS`) | 7 | NYC Climate Budgeting Report: Resiliency Exp (`7n9x-tbtd`) | 2026-05-19 |
| 0.535 | Municipal waste generated (`EN_MWT_GENV`) | 19 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.532 | Implementation of standard accounting tools to monitor the (`ST_EEV_STDACCT`) | 16 | Building Auditing Report (`9cgq-8a58`) | 2026-04-01 |
| 0.532 | Beach litter items per unit of surface area (Number of ite (`EN_MAR_BEALIT_PUSA`) | 10 | Energy and Water Data Disclosure for Local L (`utpj-74fz`) | 2024-10-01 |
| 0.528 | Proportion of total government spending on essential servi (`SG_XPD_PROT`) | 24 | CBO Expense Report (`rdjw-z878`) | 2020-04-25 |
| 0.527 | Tuberculosis incidence (`SH_TBS_INCD`) | 25 | DOHMH Tuberculosis Surveillance: Data from t (`ax85-bzte`) | 2024-11-19 |
| 0.527 | Fossil-fuel subsidies (consumption and production) (`ER_FFS_CMPT_CD`) | 15 | Office of Climate and Sustainability: 2019 F (`psr5-vz6y`) | 2024-01-24 |
| 0.524 | Maximum reservoir water area as a proportion of total land (`EN_RSRV_MXWAP`) | 23 | Census Demographics at the Neighborhood Tabu (`rnsn-acs2`) | 2020-02-08 |
| 0.52 | Proportion of total government spending on essential servi (`SD_XPD_ESED`) | 7 | Capital Projects Dashboard - Citywide Budget (`qj5n-h5qp`) | 2026-07-15 |
| 0.52 | Proportion of people with secure tenure rights to land out (`SP_LGL_LNDSTR`) | 7 | Census Demographics at the Neighborhood Tabu (`rnsn-acs2`) | 2020-02-08 |
| 0.516 | Permanent water area of lakes and rivers as a proportion o (`EN_LKRV_PWAP`) | 23 | Census Demographics at the Neighborhood Tabu (`rnsn-acs2`) | 2020-02-08 |
| 0.514 | Annual growth of final consumption expenditure of househol (`NE_CON_PRVT_KD_ZG`) | 23 | NYCHA Resident Data Book Summary (`5r5y-pvs3`) | 2025-08-01 |
| 0.513 | Number of companies publishing sustainability reports with (`EN_SCP_FRMN`) | 9 | Archaeology Reports Database (`fuzb-9jre`) | 2026-07-07 |
| 0.511 | Countries that have legislative, administrative and policy (`ER_CBD_ABSCLRHS`) | 5 | Office of Labor Policy & Standards Workplace (`2z24-2htf`) | 2025-04-22 |
| 0.51 | Ratio of non-performing loans (net of provisions) to capit (`FI_FSI_FSKNL`) | 16 | City Council Capital Budget (`t474-a92g`) | 2025-12-30 |
| 0.507 | Fossil-fuel subsidies (consumption and production) per cap (`ER_FFS_CMPT_PC_CD`) | 15 | Water Consumption in the City of New York (`ia2d-e54m`) | 2025-05-21 |
| 0.506 | Participation rate in organized learning (one year before  (`SE_PRE_PARTN`) | 11 | 2021 City Council October Attendance (`6ewv-5j4c`) | 2024-11-26 |
| 0.505 | Adjusted gender parity index for participation rate in org (`SE_GPI_PTNPRE`) | 11 | 2019-2020 Local Law 102 Physical Education R (`gf36-w2jr`) | 2024-11-26 |
| 0.504 | Hazardous waste generated (`EN_HAZ_GENV`) | 7 | Wastewater Co-digestion and Biogas-to-grid P (`b3mq-yvvr`) | 2026-08-20 |
| 0.503 | Seasonal water area of lakes and rivers (`EN_LKRV_SWAN`) | 23 | Recreational Boating Permits (`idfb-y78n`) | 2020-02-08 |
| 0.503 | Average remittance costs of sending $200 for a sending cou (`SI_RMT_COST_SND`) | 11 | Expense Budget Funding - All Source (`39g5-gbp3`) | 2026-07-08 |
| 0.502 | Number of people affected by disasters (`VC_DSR_AFFCT`) | 7 | New York City's Flood Vulnerability Index (`mrjc-v9pm`) | 2026-04-21 |

*Showing the top 60 of 50 unmapped candidates. Regenerate with `python3 probe/match_nyc.py`.*
