---
layout: default
title: Indicators the US does not report — 2026-09-17
---

# What NYC can say internationally that the United States cannot

The UN graph is national-level: a city can only ever be placed against countries. For **130 of the 442 usable SDG indicators the United States reports nothing at all** — and on those, *NYC vs the US* is not a weaker comparison than *NYC vs the world*. It is the only one available, and the US is not in it.

Of those, **67 are judged city-scoped** by the embedding classifier in `probe/scope.py` — and **28 of them are not**, because their subject is a *country* rather than a place that can hold a value. **39 survive** and are listed below.

**38 have a peer group of 15+ reporting countries**, which is the column that decides whether a placement means anything. The rest are listed too, with their true count.

> **This is a worksheet, not a crosswalk.** Under [comparability spec v0.1](https://sarapis.github.io/undatacommons-nyc/spec/) a grade is a human judgment, so every row here is `graded: false`. The NYC candidates are proposals from an embedding matcher whose precision on hand-read lists is roughly half.

## Removed: the subject is a country, not a place

The scope classifier reads an indicator's *topic* — health, water, education — and judges it municipal. It cannot see that *"extent to which countries have laws and regulations that guarantee…"* is not a quantity a city can have. **28 rows** were removed on a lexical rule, which is stated here so it can be argued with:

| Count | Indicator family |
|---:|---|
| 18 | Extent to which countries have laws and regulations  |
| 3 | Extent to which global citizenship education and edu |
| 1 | Amount of tracked re-imported Environmentally Sound  |
| 1 | Total inbound official flows for infrastructure |
| 1 | International financial flows to developing countrie |
| 1 | Degree of implementation of international instrument |
| 1 | Countries with users/communities participating in pl |
| 1 | Countries with procedures in law or policy for parti |
| 1 | Monetary amount committed to public-private partners |

Eighteen are one family — the SDG 5.6.2 legal provisions — and the matcher paired every one of them with NYC's *Local Law 37/2011 Temporary Housing Assistance*, on the token "Law". A worksheet that shipped them would have wasted a reviewer's afternoon before they reached anything real.

Every row below was re-checked against the country observations: **none of them has a single United States datapoint.** The screening proxy and the data agree.

## The worksheet

| Indicator | SDG series | Countries | Years | Unit | Best NYC candidate |
|---|---|---:|---|---|---|
| Proportion of population living below the national poverty lin | `SI_POV_NAHC` | 156 | 2000–2024 | `Percent` | Census Demographics at the Neighborhoo (0.563) |
| Number of missing persons due to disaster | `VC_DSR_MISS` | 152 | 2005–2025 | `COUNT` | *DHS Daily Report (Historical) (0.423, below floor)* |
| Number of new HIV infections per 1,000 uninfected population | `SH_HIV_INCD` | 146 | 2000–2024 | `RATIO_COUNT_PER_1000_C` | HIV/AIDS Diagnoses by Neighborhood, Se (0.597) |
| Employed persons in the tourism industries (number) | `ST_EMP_TRSMN` | 144 | 2008–2024 | `COUNT` | *NYC Business Acceleration Business (0.437, below floor)* |
| Prevalence rate of bribery | `IU_COR_BRIB` | 140 | 2004–2024 | `Percent` | *DOHMH HIV/AIDS Annual Report (0.404, below floor)* |
| Number of undernourished people | `SN_ITK_DEFCN` | 138 | 2001–2023 | `COUNT` | *2017-18 Financial Services for NYC (0.273, below floor)* |
| Municipal waste collected | `EN_MWT_COLLV` | 133 | 2000–2023 | `WEIGHT_TN` | Recycling Diversion and Capture Rates (0.633) |
| Number of people whose livelihoods were disrupted or destroyed | `VC_DSR_PDLN` | 122 | 2005–2025 | `COUNT` | *TLC Vehicles Involved in Crashes ( (0.34, below floor)* |
| Proportion of land that is degraded over total land area | `AG_LND_DGRD` | 121 | 2015–2019 | `Percent` | Primary Land Use Tax Lot Output (PLUTO (0.518) |
| Proportion of population with basic handwashing facilities on  | `SH_SAN_HNDWSH` | 120 | 2000–2024 | `Percent` | *Radiation Producing Equipment (0.426, below floor)* |
| [World Bank] Proportion of population covered by social insura | `SI_COV_SOCINS` | 119 | 1999–2024 | `Percent` | *Directory Of Unsheltered Street Ho (0.444, below floor)* |
| Direct economic loss to cultural heritage damaged or destroyed | `VC_DSR_CHLN` | 117 | 2005–2024 | `CR_USD` | *Recoupment for Damaged City-owned  (0.394, below floor)* |
| Number of destroyed or damaged health facilities attributed to | `VC_DSR_HFDN` | 116 | 2005–2025 | `COUNT` | *TLC Vehicles Involved in Crashes ( (0.416, below floor)* |
| Malaria incidence per 1,000 population at risk | `SH_STA_MALR` | 109 | 2000–2024 | `RATIO_COUNT_PER_1000_C` | Projected Population 2010-2040 - Summa (0.477) |
| Hazardous waste generated per unit of GDP | `EN_HAZ_GENGDP` | 107 | 2000–2024 | `RATIO_WEIGHT_KG_PER_CR` | Wastewater Co-digestion and Biogas-to- (0.531) |
| Percentage of bloodstream infection due to methicillin-resista | `SH_BLD_MRSA` | 98 | 2016–2022 | `Percent` | *DOHMH Covid-19 Milestone Data: Per (0.438, below floor)* |
| Hazardous waste exported | `EN_HAZ_EXP` | 97 | 2000–2024 | `WEIGHT_TN` | DSNY Disposal Sites Used by Facilities (0.521) |
| Total waste generation | `EN_TWT_GENV` | 97 | 2000–2023 | `WEIGHT_TN` | DSNY Waste Characterization - Comparat (0.515) |
| Percentage of bloodstream infection due to Escherichia coli re | `SH_BLD_ECOLI` | 97 | 2016–2022 | `Percent` | Drinking Water Quality Distribution Mo (0.48) |
| Proportion of results indicators which will be monitored using | `SG_PLN_RECRIMON` | 96 | 2016–2026 | `Percent` | Evaluation and Monitoring Reports for  (0.597) |
| Total wastewater treated | `EN_WWT_TREAT` | 94 | **2022 only** | `RATIO_VOL_M3_PER_TIME_` | Watershed Water Quality - Wastewater (0.542) |
| Hazardous waste treated or disposed | `EN_HAZ_TRTDISV` | 93 | 2000–2024 | `WEIGHT_TN` | Dewatered Solids and Biosolids Allocat (0.51) |
| Labour share of GDP | `SL_EMP_GTOTL` | 93 | 2004–2025 | `Percent` | *Personal Income By AGI Range (0.409, below floor)* |
| Proportion of hazardous waste that is treated or disposed | `EN_HAZ_TRTDISR` | 88 | 2000–2024 | `Percent` | Dewatered Solids and Biosolids Allocat (0.506) |
| Hazardous waste imported | `EN_HAZ_IMP` | 85 | 2000–2024 | `WEIGHT_TN` | DSNY Disposal Sites Used by Facilities (0.492) |
| Proportion of groundwater bodies with good ambient water quali | `EN_H2O_GRAMBQ` | 84 | 2017–2023 | `Percent` | Watershed Water Quality - Limnology (0.516) |
| Total wastewater generated | `EN_WWT_GEN` | 84 | **2022 only** | `RATIO_VOL_M3_PER_TIME_` | Wastewater Co-digestion and Biogas-to- (0.586) |
| Proportion of population who believe decision-making is inclus | `IU_DMK_INCL` | 83 | 2015–2025 | `Percent` | 2015-2016 Demographic Data - Diversity (0.48) |
| Total public expenditure per capita on cultural and natural he | `GB_XPD_CULNAT_PB` | 77 | 2017–2024 | `CR_USD_PPP` | *City of New York Municipal Solar-R (0.418, below floor)* |
| Proportion of population living in multidimensional poverty | `SD_MDP_MUHC` | 76 | 2010–2024 | `Percent` | Census Demographics at the Neighborhoo (0.518) |
| [World Bank] Proportion of population covered by labour market | `SI_COV_LMKT` | 76 | 2002–2024 | `Percent` | New York City Population By Community  (0.479) |
| Proportion of wastewater treated | `EN_WWT_TREATR` | 72 | **2022 only** | `Percent` | Dewatered Solids and Biosolids Allocat (0.519) |
| Extent of human made wetlands | `EN_WBE_HMWTL` | 55 | 2021–2025 | `AREA_KM2` | NYC Wetlands (0.497) |
| Average income of small-scale food producers, at purchasing-po | `SI_AGR_SSFP` | 51 | 2001–2024 | `CR_USD_PPP` | Income By Type Of Income And AGI Range (0.524) |
| Average income of large-scale food producers, at purchasing-po | `SI_AGR_LSFP` | 50 | 2001–2024 | `CR_USD_PPP` | Income By Type Of Income And AGI Range (0.534) |
| Proportion of population who say that overall they are satisfi | `SP_PSR_OSATIS_GOV` | 46 | 2015–2025 | `Percent` | 2013 - 2014 School Survey Data (0.513) |
| Proportion of population who say that overall they are satisfi | `SP_PSR_OSATIS_SEC` | 44 | 2015–2025 | `Percent` | 2013 - 2014 School Survey Data (0.565) |
| Proportion of population subjected to physical violence in the | `VC_VOV_PHYL` | 23 | 2011–2024 | `Percent` | New York City Population by Borough, 1 (0.451) |
| Proportion of population subjected to psychological violence i | `VC_VOV_PSYCHL` | 13 ⚠ | 2013–2024 | `Percent` | Youth Risk Behavior Survey (Middle Sch (0.459) |

⚠ = fewer than 15 reporting countries; a placement among them says little. **A single year** supports a level comparison and not a trend — 3 of these have one year only, which is the finding that removed road safety as our headline demo. A candidate *in italics* scores below 0.45, the floor under which a proposal is noise.

## The strongest rows, in detail

### Proportion of population living below the national poverty line

`undata/sdg/SI_POV_NAHC` · **156 countries** · 2000–2024 · 1,038 observations · unit `Percent` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Census Demographics at the Neighborhood Tabulation Area (NTA) level** — `rnsn-acs2`, score 0.563, z 4.63
- **Directory Of Unsheltered Street Homeless To General Population Ratio 2009** — `x56h-7iwp`, score 0.497, z 3.84
- **New York City Population By Community Districts** — `xi7c-iiu2`, score 0.497, z 3.84

### Number of missing persons due to disaster

`undata/sdg/VC_DSR_MISS` · **152 countries** · 2005–2025 · 1,489 observations · unit `COUNT` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **DHS Daily Report (Historical)** — `dwrg-kzni`, score 0.423, z 3.89
- **DHS Daily Report** — `k46n-sa2m`, score 0.417, z 3.8
- **2018-2019 Daily Attendance** — `x3bb-kg5j`, score 0.417, z 3.8

### Number of new HIV infections per 1,000 uninfected population

`undata/sdg/SH_HIV_INCD` · **146 countries** · 2000–2024 · 3,565 observations · unit `RATIO_COUNT_PER_1000_COUNT_POP_UNINFECTED` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **HIV/AIDS Diagnoses by Neighborhood, Sex, and Race/Ethnicity (Historical)** — `ykvb-493p`, score 0.597, z 5.55
- **HIV/AIDS Diagnoses by Neighborhood, Age Group, and Race/Ethnicity (Historical)** — `dxnu-p2qd`, score 0.59, z 5.46
- **DOHMH HIV/AIDS Annual Report** — `fju2-rdad`, score 0.519, z 4.53

### Employed persons in the tourism industries (number)

`undata/sdg/ST_EMP_TRSMN` · **144 countries** · 2008–2024 · 1,115 observations · unit `COUNT` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **NYC Business Acceleration Businesses Served and Jobs Created** — `9b9u-8989`, score 0.437, z 3.6
- **Local Law 18 Pay and Demographics Report - Agency Report Table** — `423i-ukqr`, score 0.435, z 3.58
- **Resident Economic Empowerment and Sustainability (REES) for NYCHA Residents – Council District - Local Law 163** — `h65x-gk9r`, score 0.425, z 3.43

### Prevalence rate of bribery

`undata/sdg/IU_COR_BRIB` · **140 countries** · 2004–2024 · 279 observations · unit `Percent` · screened AMBER

Candidate NYC datasets (proposals, ungraded):

- **DOHMH HIV/AIDS Annual Report** — `fju2-rdad`, score 0.404, z 3.42
- **Policy and Procedure Recommendations (PPR) Portal** — `jstn-jaut`, score 0.371, z 2.97
- **Local Law 33 - Security Indicators Report** — `2wuc-x56b`, score 0.371, z 2.96

### Number of undernourished people

`undata/sdg/SN_ITK_DEFCN` · **138 countries** · 2001–2023 · 2,710 observations · unit `COUNT` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **2017-18 Financial Services for NYCHA Residents - Local Law 163** — `g4tm-nibn`, score 0.273, z 3.57
- **DOHMH Cryptosporidiosis by Race/Ethnicity, Age Group, and Borough of Residence** — `fkec-mjr6`, score 0.272, z 3.56
- **Projected Public School Ratio** — `n7ta-pz8k`, score 0.261, z 3.35

### Municipal waste collected

`undata/sdg/EN_MWT_COLLV` · **133 countries** · 2000–2023 · 1,909 observations · unit `WEIGHT_TN` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Recycling Diversion and Capture Rates** — `gaq9-z3hz`, score 0.633, z 6.31
- **Location of Disposal Facilities and Sites Used for DSNY-Managed Waste** — `ufxk-pq9j`, score 0.564, z 5.35
- **DSNY Waste Characterization 2023 - Main Sort Results** — `bpea-2i5q`, score 0.559, z 5.28

### Number of people whose livelihoods were disrupted or destroyed, attributed to disasters

`undata/sdg/VC_DSR_PDLN` · **122 countries** · 2005–2025 · 1,051 observations · unit `COUNT` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **TLC Vehicles Involved in Crashes (Local Law 31)** — `5esv-8c3f`, score 0.34, z 4.79
- **Sandy Inundation Zone** — `5xsi-dfpx`, score 0.33, z 4.62
- **Youth Count** — `qx6a-vcwx`, score 0.306, z 4.25

### Proportion of land that is degraded over total land area

`undata/sdg/AG_LND_DGRD` · **121 countries** · 2015–2019 · 240 observations · unit `Percent` · screened AMBER

Candidate NYC datasets (proposals, ungraded):

- **Primary Land Use Tax Lot Output (PLUTO)** — `64uk-42ks`, score 0.518, z 4.17
- **Census Demographics at the Neighborhood Tabulation Area (NTA) level** — `rnsn-acs2`, score 0.5, z 3.96
- **Suitability of City-Owned and Leased Property for Urban Agriculture (LL 48 of 2011)** — `4e2n-s75z`, score 0.457, z 3.47

### Proportion of population with basic handwashing facilities on premises

`undata/sdg/SH_SAN_HNDWSH` · **120 countries** · 2000–2024 · 1,792 observations · unit `Percent` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Radiation Producing Equipment** — `i595-2byq`, score 0.426, z 3.76
- **NYC Pool Inspections** — `3kfa-rvez`, score 0.42, z 3.67
- **DOHMH HIV Service Directory** — `pwts-g83w`, score 0.376, z 3.05

### [World Bank] Proportion of population covered by social insurance programs

`undata/sdg/SI_COV_SOCINS` · **119 countries** · 1999–2024 · 557 observations · unit `Percent` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Directory Of Unsheltered Street Homeless To General Population Ratio 2009** — `x56h-7iwp`, score 0.444, z 3.26
- **Equitable Health Systems - Health Insurance Enrollment** — `gfej-by6h`, score 0.441, z 3.22
- **Census Demographics at the Neighborhood Tabulation Area (NTA) level** — `rnsn-acs2`, score 0.436, z 3.16

### Direct economic loss to cultural heritage damaged or destroyed attributed to disasters

`undata/sdg/VC_DSR_CHLN` · **117 countries** · 2005–2024 · 793 observations · unit `CR_USD` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Recoupment for Damaged City-owned Property** — `68k5-hdzw`, score 0.394, z 6.02
- **TLC Vehicles Involved in Crashes (Local Law 31)** — `5esv-8c3f`, score 0.318, z 4.61
- **Sandy Inundation Zone** — `5xsi-dfpx`, score 0.301, z 4.3

### Number of destroyed or damaged health facilities attributed to disasters

`undata/sdg/VC_DSR_HFDN` · **116 countries** · 2005–2025 · 628 observations · unit `COUNT` · screened AMBER

Candidate NYC datasets (proposals, ungraded):

- **TLC Vehicles Involved in Crashes (Local Law 31)** — `5esv-8c3f`, score 0.416, z 5.02
- **Staff Injuries - Class A Injuries** — `7hi3-kaps`, score 0.396, z 4.7
- **Construction-Related Incidents** — `bf97-mjsy`, score 0.375, z 4.36

### Malaria incidence per 1,000 population at risk

`undata/sdg/SH_STA_MALR` · **109 countries** · 2000–2024 · 2,725 observations · unit `RATIO_COUNT_PER_1000_COUNT_POP` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Projected Population 2010-2040 - Summary** — `ph5g-sr3v`, score 0.477, z 4.31
- **Mosquito control events in NYC – Adult Mosquito Truck Spraying and Aerial Larviciding Events** — `msid-end4`, score 0.473, z 4.26
- **SARS-CoV-2 concentrations measured in NYC Wastewater** — `f7dc-2q9f`, score 0.463, z 4.12

### Hazardous waste generated per unit of GDP

`undata/sdg/EN_HAZ_GENGDP` · **107 countries** · 2000–2024 · 1,140 observations · unit `RATIO_WEIGHT_KG_PER_CR_USD_K` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Wastewater Co-digestion and Biogas-to-grid Performance Indicators** — `b3mq-yvvr`, score 0.531, z 4.6
- **Energy and Water Data Disclosure for Local Law 84 2015 (Data for Calendar Year 2014)** — `nbun-wekj`, score 0.512, z 4.35
- **Energy and Water Data Disclosure for Local Law 84 2016 (Data for Calendar Year 2015)** — `77q4-nkfh`, score 0.487, z 4.01

### Percentage of bloodstream infection due to methicillin-resistant Staphylococcus aureus (MRSA) among patients seeking care and whose blood sample is taken and tested

`undata/sdg/SH_BLD_MRSA` · **98 countries** · 2016–2022 · 404 observations · unit `Percent` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **DOHMH Covid-19 Milestone Data: Percent of NYC residents tested who tested positive** — `7434-7ua6`, score 0.438, z 5.5
- **DOHMH Covid-19 Milestone Data: Daily Number of People Admitted to NYC hospitals for Covid-19 like Illness** — `sj3k-gzyx`, score 0.39, z 4.82
- **DOHMH COVID-19 Antibody-by-Borough** — `x98t-3bbk`, score 0.347, z 4.22

### Hazardous waste exported

`undata/sdg/EN_HAZ_EXP` · **97 countries** · 2000–2024 · 1,148 observations · unit `WEIGHT_TN` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **DSNY Disposal Sites Used by Facilities by Year** — `99xv-he3n`, score 0.521, z 6.67
- **DSNY Commercial Waste Zones** — `8ev8-jjxq`, score 0.437, z 5.43
- **Wastewater Co-digestion and Biogas-to-grid Performance Indicators** — `b3mq-yvvr`, score 0.426, z 5.26

### Total waste generation

`undata/sdg/EN_TWT_GENV` · **97 countries** · 2000–2023 · 1,043 observations · unit `WEIGHT_TN` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **DSNY Waste Characterization - Comparative Results** — `bibp-6ff7`, score 0.515, z 5.18
- **Recycling Diversion and Capture Rates** — `gaq9-z3hz`, score 0.508, z 5.07
- **DSNY Waste Characterization 2023 - Main Sort Results** — `bpea-2i5q`, score 0.496, z 4.92

### Percentage of bloodstream infection due to Escherichia coli resistant to 3rd-generation cephalosporin (e.g., ESBL- E. coli) among patients seeking care and whose blood sample is taken and tested

`undata/sdg/SH_BLD_ECOLI` · **97 countries** · 2016–2022 · 413 observations · unit `Percent` · screened GREEN

Candidate NYC datasets (proposals, ungraded):

- **Drinking Water Quality Distribution Monitoring Data** — `bkwf-xfky`, score 0.48, z 5.77
- **Harbor Water Quality** — `5uug-f49n`, score 0.405, z 4.6
- **DOHMH Covid-19 Milestone Data: Percent of NYC residents tested who tested positive** — `7434-7ua6`, score 0.392, z 4.4

### Proportion of results indicators which will be monitored using government sources and monitoring systems - data by recipient

`undata/sdg/SG_PLN_RECRIMON` · **96 countries** · 2016–2026 · 203 observations · unit `Percent` · screened AMBER

Candidate NYC datasets (proposals, ungraded):

- **Evaluation and Monitoring Reports for Program Sites** — `9f5n-qdib`, score 0.597, z 4.29
- **Monthly Performance Management Reports (includes Corruption Lectures and Customer Service indicators)** — `i8ua-bnkj`, score 0.583, z 4.12
- **OneNYC Indicators (Historical)** — `f34v-uffx`, score 0.561, z 3.87

## Reproducing

```bash
python3 probe/us_silent.py
```

Reads `probe/cache/screened.json` and the cached corpus sweep in `probe/cache/smell-raw.json`; no network calls.

