---
layout: default
title: Crosswalk candidates — 2026-09-14
---

# Crosswalk candidates — 2026-09-14

Every usable SDG indicator (442 of 689 — graded GREEN, AMBER or RANK-ONLY against a six-country coverage panel), searched against the NYC Open Data catalog.

179 were excluded before searching as inherently national — ODA, debt service, treaties, tariffs, fisheries and similar. A city does not publish them and matching could only yield false positives. The classifier scores precision 0.83 at perfect recall on 50 hand-labelled cases (`probe/scope_eval.json`), against 0.69 for the keyword list it replaced.

Retrieval: **embedding**. Embedding search over the full 2,400-dataset catalog (name, description, columns, tags, category), which on our seven verified pairs put the correct dataset at median rank **23** versus **1535** for keyword overlap.

**This is a shortlist for human review, not a set of mappings.** Similarity surfaces a candidate; it cannot decide comparability. Two of those seven verified pairs stay unfindable at any rank because the mapping depends on what is *inside* a dataset — NYC's homicide series is offence code 101 inside 'NYPD Complaint Data Historic', which its metadata never mentions. Promoting a row into `probe/crosswalk.json` means writing the grade and the reason by hand.

- 442 indicators usable on the UN side
- 110 have at least one NYC dataset above the 0.5 similarity floor
- **106 are not yet in the crosswalk**

| Score | SDG indicator | Coverage | Candidate NYC dataset | Updated |
|---|---|---:|---|---|
| 0.702 | Municipal waste recycled (`EN_MWT_RCYV`) | 3/6 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.634 | Number of victims of intentional homicide (`VC_IHR_PSRCN`) | 6/6 | Domestic Violence Homicide Incidents in the  (`u97r-kgca`) | 2024-01-31 |
| 0.631 | Municipal waste collected (`EN_MWT_COLLV`) | 5/6 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.63 | Wetlands area (`EN_WBE_WTLN`) | 6/6 | NYC Wetlands (`p48c-iqtu`) | 2026-01-06 |
| 0.627 | Total electronic waste collected (`EN_EWT_COLLV`) | 2/6 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.622 | Growth rates of household expenditure or income per capita (`SI_HEI_TOTL`) | 5/6 | Income By Type Of Income And AGI Range (`gffu-ps8j`) | 2019-02-11 |
| 0.621 | Number of deaths rate due to road traffic injuries (`SH_STA_TRAFN`) | 6/6 | Collisions involving vehicles managed by Dep (`knr6-vurn`) | 2023-10-24 |
| 0.617 | Share of renewable energy in the total final energy consum (`EG_FEC_RNEW`) | 6/6 | Local Law 84 Monthly Data (Calendar Year) (`fvp3-gcb2`) | 2025-11-25 |
| 0.609 | Fixed broadband subscriptions per 100 inhabitants (`IT_NET_BBND`) | 6/6 | Broadband Adoption and Infrastructure by Cou (`cgwq-3ie6`) | 2022-09-23 |
| 0.607 | Countries that have conducted at least one population and  (`SG_REG_CENSUSN`) | 5/6 | New York City Population By Community Distri (`xi7c-iiu2`) | 2024-11-12 |
| 0.607 | Police reporting rate for sexual violence in the previous  (`VC_PRR_SEX_VIO`) | 2/6 | ENDGBV: The Intersection of Domestic Violenc (`2rb7-7eqa`) | 2024-01-31 |
| 0.606 | Number of new HIV infections per 1,000 uninfected populati (`SH_HIV_INCD`) | 5/6 | HIV/AIDS Diagnoses by Neighborhood, Sex, and (`ykvb-493p`) | 2026-03-13 |
| 0.606 | Police reporting rate for sexual assault in the previous 1 (`VC_PRR_SEXV`) | 3/6 | ENDGBV: The Intersection of Domestic Violenc (`2rb7-7eqa`) | 2024-01-31 |
| 0.601 | Proportion of results indicators which will be monitored u (`SG_PLN_RECRIMON`) | 2/6 | Monthly Performance Management Reports (incl (`i8ua-bnkj`) | 2022-05-09 |
| 0.59 | Performance index of data Infrastructure (Pillar 5 of Stat (`IQ_SPI_PIL5`) | 6/6 | PMMR Performance Indicators FY2013-15 (Histo (`n6uf-ruxa`) | 2023-11-30 |
| 0.588 | Gross public sector debt, Central Government, as a proport (`DP_DOD_DLD2_CR_CG_Z1`) | 4/6 | Debt Burden (`hdie-5bdv`) | 2026-05-19 |
| 0.585 | Proportion of total government spending on essential servi (`SG_XPD_EDUC`) | 6/6 | CBO Expense Report (`rdjw-z878`) | 2020-04-25 |
| 0.585 | Proportion of total government spending on essential servi (`SG_XPD_ESSRV`) | 5/6 | CBO Expense Report (`rdjw-z878`) | 2020-04-25 |
| 0.584 | Annual growth of final consumption expenditure of the gene (`NE_CON_GOVT_KD_ZG`) | 6/6 | Mayor's Management Report Spending and Budge (`2jrp-puwz`) | 2025-09-24 |
| 0.584 | Proportion of results indicators which will be monitored u (`SG_PLN_PRVRIMON`) | 2/6 | Monthly Performance Management Reports (incl (`i8ua-bnkj`) | 2022-05-09 |
| 0.578 | Performance index of data sources (Pillar 4 of Statistical (`IQ_SPI_PIL4`) | 6/6 | PMMR Performance Indicators FY2013-15 (Histo (`n6uf-ruxa`) | 2023-11-30 |
| 0.576 | Food waste (`AG_FOOD_WST`) | 6/6 | Wastewater Co-digestion and Biogas-to-grid P (`b3mq-yvvr`) | 2026-08-20 |
| 0.576 | Extent to which global citizenship education and education (`SE_GCEDESD_TED`) | 3/6 | 2015 - 2016 Final Class Size Report Pupil-to (`rtws-c2ai`) | 2024-11-26 |
| 0.573 | Total bugetary revenue of the central government as a prop (`GR_G14_GDP`) | 6/6 | Debt Burden (`hdie-5bdv`) | 2026-05-19 |
| 0.564 | Proportion of population living below the national poverty (`SI_POV_NAHC`) | 4/6 | Census Demographics at the Neighborhood Tabu (`rnsn-acs2`) | 2020-02-08 |
| 0.564 | Countries with users/communities participating in planning (`ER_WAT_PART`) | 4/6 | Safety Events (`3vyj-dkjt`) | 2026-09-11 |
| 0.563 | Police reporting rate for physical violence in the previou (`VC_PRR_PHY_VIO`) | 4/6 | Local Law 33 - Security Indicators Report (`2wuc-x56b`) | 2021-11-03 |
| 0.563 | Police reporting rate for robbery in the previous 12 month (`VC_PRR_ROBB`) | 3/6 | DOP Adult Probationers Rearrested As A Perce (`arhf-esqb`) | 2026-08-04 |
| 0.561 | Total wastewater generated (`EN_WWT_GEN`) | 3/6 | Watershed Water Quality - Wastewater (`icbf-663g`) | 2025-05-02 |
| 0.558 | Minimum reservoir water area as a proportion of total land (`EN_RSRV_MNWAP`) | 6/6 | Census Demographics at the Neighborhood Tabu (`rnsn-acs2`) | 2020-02-08 |
| 0.556 | Installed renewable electricity-generating capacity (`EG_EGY_RNEW`) | 6/6 | City of New York Municipal Solar-Readiness A (`cfz5-6fvh`) | 2026-04-16 |
| 0.554 | Proportion of total government spending on essential servi (`SG_XPD_HLTH`) | 6/6 | CBO Expense Report (`rdjw-z878`) | 2020-04-25 |
| 0.553 | Electronic waste collected per capita (`EN_EWT_COLLPCAP`) | 2/6 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.551 | Carbon dioxide emissions from fuel combustion (`EN_ATM_CO2`) | 6/6 | Office of Climate and Sustainability: 2019 F (`psr5-vz6y`) | 2024-01-24 |
| 0.551 | Police reporting rate for physical assault in the previous (`VC_PRR_PHYV`) | 3/6 | ENDGBV: The Intersection of Domestic Violenc (`2rb7-7eqa`) | 2024-01-31 |
| 0.549 | Proportion of the population with positive out-of-pocket h (`SH_OOP_XPD_EARNNET40`) | 6/6 | NYCHA Resident Data Book Summary (`5r5y-pvs3`) | 2025-08-01 |
| 0.549 | Suicide mortality rate (`SH_STA_SCIDE`) | 6/6 | New York City Leading Causes of Death (`jb7j-dtam`) | 2026-01-27 |
| 0.548 | Number of deaths due to disaster (`VC_DSR_MORT`) | 5/6 | New York City Leading Causes of Death (`jb7j-dtam`) | 2026-01-27 |
| 0.548 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHES2`) | 4/6 | Local Law 37/2011 - Temporary Housing Assist (`bdft-9t6c`) | 2023-08-04 |
| 0.548 | Total electronic waste generated (`EN_EWT_GENV`) | 2/6 | DSNY Waste Characterization - Comparative Re (`bibp-6ff7`) | 2024-05-02 |
| 0.546 | Tourism direct GDP as a proportion of total GDP (`ST_GDP_ZS`) | 5/6 | Debt Burden (`hdie-5bdv`) | 2026-05-19 |
| 0.545 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHES1`) | 4/6 | Local Law 37/2011 - Temporary Housing Assist (`bdft-9t6c`) | 2023-08-04 |
| 0.544 | Land area (`AG_LND_TOTL`) | 6/6 | Functional Parkland (`xhvt-s4va`) | 2026-08-16 |
| 0.543 | Number of full-time-equivalent researchers per million inh (`GB_POP_SCIERD`) | 6/6 | Full-Time And Full-Time Equivalent Staffing  (`2t2c-qih9`) | 2026-07-08 |
| 0.542 | Countries with procedures in law or policy for participati (`ER_WAT_PRDU`) | 4/6 | Safety Events (`3vyj-dkjt`) | 2026-09-11 |
| 0.541 | Domestic material consumption per capita (`EN_MAT_DOMCMPC`) | 6/6 | Water Consumption in the City of New York (`ia2d-e54m`) | 2025-05-21 |
| 0.541 | Total greenhouse gas emissions (including land use, land-u (`EN_ATM_GHGT_WLU`) | 5/6 | Energy and Water Data Disclosure for Local L (`wcm8-aq5w`) | 2024-10-01 |
| 0.54 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHES4`) | 5/6 | DOHMH HIV/AIDS Annual Report (`fju2-rdad`) | 2025-06-24 |
| 0.539 | Proportion of local governments that adopt and implement l (`SG_DSR_SILS`) | 6/6 | NYC Climate Budgeting Report: Resiliency Exp (`7n9x-tbtd`) | 2026-05-19 |
| 0.538 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHEC1`) | 4/6 | Local Law 37/2011 - Temporary Housing Assist (`bdft-9t6c`) | 2023-08-04 |
| 0.535 | Municipal waste generated (`EN_MWT_GENV`) | 4/6 | Recycling Diversion and Capture Rates (`gaq9-z3hz`) | 2020-02-08 |
| 0.532 | Beach litter items per unit of surface area (Number of ite (`EN_MAR_BEALIT_PUSA`) | 6/6 | Energy and Water Data Disclosure for Local L (`utpj-74fz`) | 2024-10-01 |
| 0.532 | Implementation of standard accounting tools to monitor the (`ST_EEV_STDACCT`) | 5/6 | Building Auditing Report (`9cgq-8a58`) | 2026-04-01 |
| 0.532 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHEC9`) | 4/6 | 2020-2021 Local Law 231 Training Data (`rxj2-pb49`) | 2024-11-26 |
| 0.532 | Proportion of population living in multidimensional povert (`SD_MDP_MUHC`) | 2/6 | Census Demographics at the Neighborhood Tabu (`rnsn-acs2`) | 2020-02-08 |
| 0.531 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHEC8`) | 4/6 | 2020-2021 Local Law 231 Training Data (`rxj2-pb49`) | 2024-11-26 |
| 0.53 | Forest area certified under an independently verified cert (`AG_LND_FRSTCERT`) | 6/6 | Civil Service List Certification (`a9md-ynri`) | 2026-09-14 |
| 0.53 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHE`) | 4/6 | Local Law 37/2011 - Temporary Housing Assist (`bdft-9t6c`) | 2023-08-04 |
| 0.53 | Extent to which countries have laws and regulations that g (`SH_LGR_ACSRHES3`) | 4/6 | 2020-2021 Local Law 231 Training Data (`rxj2-pb49`) | 2024-11-26 |
| 0.53 | Total waste generation (`EN_TWT_GENV`) | 2/6 | DSNY Waste Characterization - Comparative Re (`bibp-6ff7`) | 2024-05-02 |

*Showing the top 60 of 106 unmapped candidates. Regenerate with `python3 probe/match_nyc.py`.*
