---
layout: default
title: Inverse crosswalk — 2026-09-16
---

# The inverse crosswalk — 2026-09-16

Every other analysis here runs city → UN: take an SDG indicator, find the municipal dataset that matches it. That can only discover what the framework already asks about. This runs it backwards — take every dataset a city publishes, find its nearest SDG indicator, and look at what is left over.

**11,206 datasets** from **37 city portals** (language `en`), matched against **all 689 enumerated SDG indicators** — not the 442 with usable data, because a framework gap is a question about vocabulary rather than coverage.

**What a result here means.** A dataset far from every indicator means no SDG indicator's *text* is near this dataset's *text*. That is evidence about vocabulary, not proof of a conceptual gap — this project has already learned once that a null from the matcher is not evidence of absence. So the unit of evidence below is **how many independent cities** a theme appears in. A theme in thirty city catalogs is a category of municipal governance; a theme in one is that city's filing habit.

## Positive controls

Datasets from the hand-verified NYC crosswalk. These are known to correspond to an SDG indicator, so they must land in the high-affinity region. If they fall in the tail, the tail is measuring retrieval failure and nothing below is trustworthy.

**7 of 7 located · 1 fell in the tail.**

| Verified pair | NYC dataset | Affinity | Percentile | In tail? |
|---|---|---:|---:|---|
| Road traffic deaths | Motor Vehicle Collisions - Crashes | 0.627 | 99 | no |
| Child mortality (deaths) | Infant Mortality | 0.578 | 96 | no |
| Maternal mortality | Pregnancy-Associated Mortality | 0.506 | 86 | no |
| Deaths attributable to ambient air pollution | Air Quality and Health Impacts | 0.47 | 74 | no |
| Municipal waste collected | DSNY Monthly Tonnage Data | 0.438 | 60 | no |
| Intentional homicide | NYPD Complaint Data Historic | 0.425 | 54 | no |
| Inadequate housing | Housing Maintenance Code Violations | 0.375 | 24 | **YES** |

## What cities publish that the SDGs have no words for

The bottom **25% of each catalog** by affinity — 2,790 datasets. Below are the title phrases that recur across that tail, **counted by how many independent cities use them**. These are not inferred categories; they are what the cities themselves called the data.

| Cities | Datasets | Phrase |
|---:|---:|---|
| 7 | 22 | **street sweeping** |
| 7 | 7 | **fire stations** |
| 6 | 12 | **building permits** |
| 6 | 8 | **special events** |
| 6 | 7 | **zip code** |
| 5 | 8 | **business licenses** |
| 5 | 5 | **call center** |
| 5 | 5 | **bike share** |
| 5 | 5 | **bus stops** |
| 5 | 5 | **zip codes** |
| 4 | 10 | **traffic signal** |
| 4 | 6 | **bus stop** |
| 4 | 5 | **work orders** |
| 4 | 4 | **street name** |
| 4 | 4 | **council district** |

### In detail

**street sweeping** — 22 datasets across 7 cities

- Street Sweeping Schedule - 2018 — Chicago
- BOUNDARIES_street_sweeping_zones — Austin
- PRR 9545 - Street Sweeping 2013 - 2015 05.08.2015 — Oakland
- Street Sweeping Districts — Cambridge
- Street Sweeping Schedules — Boston


**fire stations** — 7 datasets across 7 cities

- Fire Stations — Austin
- Fire Stations — Calgary
- Fire Stations — Los Angeles
- Fire Stations — Dallas
- Fire Stations — New Orleans


**building permits** — 12 datasets across 6 cities

- Building Permits — Dallas
- Building Permits — Mesa
- Tent - Building Permits — Cambridge
- EBR Building Permits — Baton Rouge
- Last 30 days building permits — San Jose


**special events** — 8 datasets across 6 cities

- Public Programs Division Special Events — New York
- FOIA Request Log - Cultural Affairs & Special Events — Chicago
- EMS Special Events FY 2017 — Austin
- Cultural & Special Events at El Pueblo Historical Monument — Los Angeles
- Special Events Attendees — Mesa


**zip code** — 7 datasets across 6 cities

- Modified Zip Code Tabulation Areas (MODZCTA) — New York
- 2023-2025 Heat Related Deaths by Zip Code — Mesa
- ZIP Code — Baton Rouge
- MO_2010_Zip_Code_Tabulation_Areas_shp — Kansas City
- Zip Code Boundary — San Jose


**business licenses** — 8 datasets across 5 cities

- Active Credit Access Business Licenses — Austin
- Historical Occupational Business Licenses 2017 — New Orleans
- Active Business Licenses in Providence — Providence
- Business Licenses — Norfolk
- Business Licenses — Berkeley


**call center** — 5 datasets across 5 cities

- 311 Call Center Inquiry — New York
- Performance Metrics - 311 Call Center — Chicago
- 311 Call Center Service Request Data - Archived 2013-2014 — Los Angeles
- Service requests received by the Oakland Call Center (OAK 311) — Oakland
- 311 Call Center Service Requests: 2007 - March 2021 — Kansas City


**bike share** — 5 datasets across 5 cities

- Bike Share Inspections (Historical) — New York
- Metro Bike Share Trip Data — Los Angeles
- Oakland Bike Share Stations — Oakland
- Bike Share Docks — San Jose
- Bike Share 12.15 — Santa Monica


**bus stops** — 5 datasets across 5 cities

- Deprecated - ETS - Bus Stops by Landmarks — Edmonton
- KCATA Bus Stops - Deprecated — Kansas City
- Housing Bus Stops — Santa Monica
- Bus Stops — Everett
- RTS Bus Stops List Fall 2020 — Gainesville


**zip codes** — 5 datasets across 5 cities

- Zip Codes within the City of Los Angeles — Los Angeles
- ZIP Codes — Cambridge
- BT_Zip_Codes — Baton Rouge
- Zip Codes — Kansas City
- Zip Codes — Providence


**traffic signal** — 10 datasets across 4 cities

- Synchronized Traffic Signal Corridors — Austin
- Traffic Signal Signs — Calgary
- Traffic Signal Audits — Mesa
- Traffic Signal Inventory - Locations — Winnipeg


**bus stop** — 6 datasets across 4 cities

- Intercity Bus Stop Permits — New York
- CTA - Ridership - Avg. Weekday Bus Stop Boardings in October 2012 — Chicago
- Bus Stop — Baton Rouge
- Everett Transit - Bus Stop Utilization — Everett


**work orders** — 5 datasets across 4 cities

- Street Sign Work Orders — New York
- Work Orders Completed: El Pueblo Historical Monument — Los Angeles
- PRCF - Park Amenities Completed Work Orders — Mesa
- Work Orders — Norfolk


**street name** — 4 datasets across 4 cities

- Street Name Signs Work Orders (Historical) — New York
- 911 Addressing - Street Name Master List — Austin
- EBRP Street Name Changes — Baton Rouge
- Street Name — New Orleans



## The same tail, clustered by embedding

A second view, kept because it groups datasets that share no vocabulary. k-means returns *k* clusters whether or not *k* themes exist, so each carries its **coherence** — the mean cosine of its members to its own centroid. Below 0.62, a cluster is a partition rather than a theme and is marked diffuse; **14 of 40 are.** Read those as noise, not as findings.

| Coherence | Cities | Datasets | Terms | Closest SDG indicator |
|---:|---:|---:|---|---|
| 0.991 | 3 | 238 | dfs, check, speed, sign | Beach litter items per unit of surface area  |
| 0.808 | 4 | 79 | libraries, location, holds | Countries with users/communities participati |
| 0.765 | 7 | 37 | trip, hire | Number of deaths rate due to road traffic in |
| 0.739 | 19 | 81 | (no term covers a fifth of this cluster) | Countries that have national urban policies  |
| 0.737 | 10 | 52 | overlay | Number of companies publishing sustainabilit |
| 0.704 | 2 | 55 | te-des-neiges, notre-dame-de-gr, contrats, par, les | DI ILL IN |
| 0.7 | 26 | 241 | (no term covers a fifth of this cluster) | Land area |
| 0.695 | 15 | 67 | foia, request, log | Countries that have legislative, administrat |
| 0.69 | 10 | 41 | sweeping, schedule, issued, violations, street | Countries with procedures in law or policy f |
| 0.689 | 18 | 115 | (no term covers a fifth of this cluster) | Land area |
| 0.689 | 6 | 48 | arterials, arterial, lane, miles | Number of deaths rate due to road traffic in |
| 0.684 | 9 | 18 | bicycle, counts, pedestrian, bike | Number of deaths rate due to road traffic in |
| 0.682 | 10 | 38 | csb, update, telephone, seconds, less | Police reporting rate for robbery in the pre |
| 0.672 | 13 | 53 | bike, spaces, parking | Number of deaths rate due to road traffic in |
| 0.668 | 17 | 84 | (no term covers a fifth of this cluster) | Land area |
| 0.663 | 10 | 61 | (no term covers a fifth of this cluster) | Countries that have national urban policies  |
| 0.662 | 14 | 57 | (no term covers a fifth of this cluster) | FC ACC SSID |
| 0.661 | 1 | 46 | des | Coastal Eutrophication: Total Nitrogen (micr |
| 0.66 | 17 | 93 | (no term covers a fifth of this cluster) | Total wastewater generated |
| 0.659 | 15 | 105 | insight, edmonton, community | Participation rate in organized learning (on |
| 0.657 | 21 | 103 | (no term covers a fifth of this cluster) | Countries that adopt and implement constitut |
| 0.64 | 8 | 32 | homes, sales, dof, family, class | Average income of small-scale food producers |
| 0.639 | 22 | 110 | (no term covers a fifth of this cluster) | Number of deaths rate due to road traffic in |
| 0.637 | 23 | 81 | permits, building | Countries with procedures in law or policy f |
| 0.631 | 18 | 102 | (no term covers a fifth of this cluster) | Countries that have national urban policies  |
| 0.63 | 13 | 31 | zip, zones, code | Countries that have national urban policies  |
| 0.61 *(diffuse)* | 8 | 26 | (no term covers a fifth of this cluster) | Detected victims of human trafficking for fo |
| 0.606 *(diffuse)* | 3 | 103 | (no term covers a fifth of this cluster) | Number of deaths rate due to road traffic in |
| 0.605 *(diffuse)* | 12 | 45 | election, general, voting, council | Countries that adopt and implement constitut |
| 0.586 *(diffuse)* | 15 | 36 | animal, calls | Number of disruptions to basic services attr |
| 0.58 *(diffuse)* | 9 | 62 | school | Adjusted gender parity index for participati |
| 0.577 *(diffuse)* | 12 | 32 | sea, rise, inch, level | Score of adoption and implementation of nati |
| 0.575 *(diffuse)* | 11 | 37 | ems | Proportion of results indicators which will  |
| 0.571 *(diffuse)* | 18 | 47 | analytics | Proportion of results indicators drawn from  |
| 0.57 *(diffuse)* | 12 | 74 | (no term covers a fifth of this cluster) | Land area |
| 0.559 *(diffuse)* | 23 | 90 | (no term covers a fifth of this cluster) | Countries with procedures in law or policy f |
| 0.553 *(diffuse)* | 20 | 68 | (no term covers a fifth of this cluster) | Countries with users/communities participati |
| 0.544 *(diffuse)* | 10 | 15 | downloads, gtfs | Number of fixed broadband subscriptions |
| 0.541 *(diffuse)* | 17 | 40 | (no term covers a fifth of this cluster) | Countries that have legislative, administrat |
| 0.536 *(diffuse)* | 15 | 47 | employee | Employed persons in the tourism industries ( |

### The coherent clusters in detail

**dfs, check, speed, sign** — 238 datasets across 3 cities (coherence 0.991, mean affinity 0.324)

- Speed Check Sign - DFS041 — Edmonton
- Speed Limits — Calgary
- Real-Time Midblock Traffic Data — Winnipeg
- Mobile Automated Photo Enforcement Ticket Zones — Edmonton
- Speed Check Sign - DFS001 — Edmonton


**libraries, location, holds** — 79 datasets across 4 cities (coherence 0.808, mean affinity 0.326)

- Employee Overtime and Supplemental Earnings 2017 — Chicago
- Average Discount per Customer FY 2024 — Austin
- T10 Bus Travel Time — Santa Monica
- Summer of 2014, Weekly Camp, Pool and Water Park Attendance — Providence
- Employee Overtime and Supplemental Earnings 2021 — Chicago


**trip, hire** — 37 datasets across 7 cities (coherence 0.765, mean affinity 0.341)

- 2016 Green Taxi Trip Data — New York
- ETS GTFS Feed: Trip Schedule — Edmonton
- Transportation Network Providers - Trips (2023-2024) — Chicago
- Austin MetroBike Trips — Austin
- Los Angeles International Airport - Passenger Traffic By Terminal — Los Angeles


**(no term covers a fifth of this cluster)** — 81 datasets across 19 cities (coherence 0.739, mean affinity 0.322)

- VZV Speed Humps — New York
- Contour Lines LL - WGS84 — Edmonton
- zoning_pedstreet — Chicago
- USGSQQ — Austin
- DCP_HPOZ_PLY — Los Angeles


**overlay** — 52 datasets across 10 cities (coherence 0.737, mean affinity 0.339)

- Bureau of Fire Prevention - Building Summary (Historical) — New York
- Alley LL - WGS84 — Edmonton
- City of Austin Schools with Data — Austin
- Community District Boundaries — Calgary
- Jill SRF 14 08 Permit W Location — Dallas


**te-des-neiges, notre-dame-de-gr, contrats, par, les** — 55 datasets across 2 cities (coherence 0.704, mean affinity 0.317)

- Fréquentation du portail de données ouvertes — Montréal
- SanJoseandBoundaryIntersections — San Jose
- Demandes de services citoyennes (Requêtes 311) — Montréal
- Statistiques d'utilisation du site web de la Ville de Montréal (montreal.ca) — Montréal
- Liste des ensembles automatisés sur le site des Données ouvertes — Montréal


**(no term covers a fifth of this cluster)** — 241 datasets across 26 cities (coherence 0.7, mean affinity 0.346)

- 2018 Central Park Squirrel Census - Squirrel Data — New York
- Rainfall History - (2013 - 2015) — Edmonton
- Chicago Street Names — Chicago
- Credit Access Businesses — Austin
- Calgary Public Library Locations and Hours — Calgary


**foia, request, log** — 67 datasets across 15 cities (coherence 0.695, mean affinity 0.33)

- NYC Historical Vital Records: Index to Digitized Death Certificates — New York
- Memos to Council — Edmonton
- DEEL Seattle Promise Applications — Seattle
- FOIA Request Log - Police — Chicago
- Community PC Program_Number of Devices — Austin


**sweeping, schedule, issued, violations, street** — 41 datasets across 10 cities (coherence 0.69, mean affinity 0.337)

- DOF Parking Violation Codes — New York
- 311 Calls for Needles Collection — Edmonton
- 2015 Find It, Fix It Total Reports by Category — Seattle
- Street Sweeping Schedule - 2018 — Chicago
- Citation Data Portal — Oakland


**(no term covers a fifth of this cluster)** — 115 datasets across 18 cities (coherence 0.689, mean affinity 0.333)

- Parking Regulation Locations and Signs — New York
- Drainage_Pipe Segments — Edmonton
- buildings — Chicago
- Zoning Cases — Austin
- On-Street Parking Zones — Calgary



## Reproducing

```bash
python3 probe/fetch_municipal.py
python3 probe/inverse.py
```

