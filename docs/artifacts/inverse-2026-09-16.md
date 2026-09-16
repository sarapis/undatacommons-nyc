---
layout: default
title: Inverse crosswalk — 2026-09-16
---

# The inverse crosswalk — 2026-09-16

Every other analysis here runs city → UN: take an SDG indicator, find the municipal dataset that matches it. That can only discover what the framework already asks about. This runs it backwards — take every dataset a city publishes, find its nearest SDG indicator, and look at what is left over.

**11,206 datasets** from **37 city portals** (language `en`), matched against **all 519 enumerated SDG indicators** — not the 442 with usable data, because a framework gap is a question about vocabulary rather than coverage.

**What a result here means.** A dataset far from every indicator means no SDG indicator's *text* is near this dataset's *text*. That is evidence about vocabulary, not proof of a conceptual gap — this project has already learned once that a null from the matcher is not evidence of absence. So the unit of evidence below is **how many independent cities** a theme appears in. A theme in thirty city catalogs is a category of municipal governance; a theme in one is that city's filing habit.

## Positive controls

Datasets from the hand-verified NYC crosswalk. These are known to correspond to an SDG indicator, so they must land in the high-affinity region. If they fall in the tail, the tail is measuring retrieval failure and nothing below is trustworthy.

**9 of 9 located · 1 fell in the tail.**

| Expected correspondence | City | Dataset | Affinity | Percentile | In tail? |
|---|---|---|---:|---:|---|
| Road traffic deaths | New York | Motor Vehicle Collisions - Crashes | 0.627 | 99 | no |
| Child mortality (deaths) | New York | Infant Mortality | 0.578 | 96 | no |
| Maternal mortality | New York | Pregnancy-Associated Mortality | 0.506 | 86 | no |
| Fine particulate matter (PM2.5), annual mean | New York | Air Quality and Health Impacts | 0.47 | 74 | no |
| Deaths attributable to ambient air pollution | New York | Air Quality and Health Impacts | 0.47 | 74 | no |
| Proportion of municipal waste recycled | New York | DSNY Monthly Tonnage Data | 0.438 | 61 | no |
| Municipal waste collected | New York | DSNY Monthly Tonnage Data | 0.438 | 61 | no |
| Intentional homicide | New York | NYPD Complaint Data Historic | 0.425 | 55 | no |
| Inadequate housing | New York | Housing Maintenance Code Violations | 0.367 | 21 | **YES** |

## What cities publish that the SDGs have no words for

The bottom **25% of each catalog** by affinity — 2,786 datasets. Below are the title phrases that recur across that tail, **counted by how many independent cities use them**. These are not inferred categories; they are what the cities themselves called the data.

| Cities | Datasets | Phrase |
|---:|---:|---|
| 7 | 22 | **street sweeping** |
| 6 | 10 | **building permits** |
| 6 | 8 | **special events** |
| 6 | 7 | **zip code** |
| 6 | 6 | **fire stations** |
| 5 | 5 | **call center** |
| 5 | 5 | **bike share** |
| 5 | 5 | **bus stops** |
| 5 | 5 | **zip codes** |
| 4 | 7 | **business licenses** |
| 4 | 6 | **work orders** |
| 4 | 6 | **bus stop** |
| 4 | 4 | **street name** |
| 4 | 4 | **council district** |

### In detail

**street sweeping** — 22 datasets across 7 cities

- Street Sweeping Schedule - 2018 — Chicago
- BOUNDARIES_street_sweeping_zones — Austin
- PRR 9545 - Street Sweeping 2013 - 2015 05.08.2015 — Oakland
- Street Sweeping Districts — Cambridge
- Street Sweeping Schedules — Boston


**building permits** — 10 datasets across 6 cities

- Building Permits for Fiscal Year 2011 - 2012 — Dallas
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


**fire stations** — 6 datasets across 6 cities

- Fire Stations — Austin
- Fire Stations — Calgary
- Fire Stations — Los Angeles
- Fire Stations — Dallas
- Fire Stations — New Orleans


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


**business licenses** — 7 datasets across 4 cities

- Active Credit Access Business Licenses — Austin
- Historical Occupational Business Licenses 2017 — New Orleans
- Active Business Licenses in Providence — Providence
- Business Licenses — Norfolk


**work orders** — 6 datasets across 4 cities

- Street Sign Work Orders — New York
- Work Orders Completed: El Pueblo Historical Monument — Los Angeles
- PRCF - Park Amenities Completed Work Orders — Mesa
- Work Orders — Norfolk


**bus stop** — 6 datasets across 4 cities

- Intercity Bus Stop Permits — New York
- CTA - Ridership - Avg. Weekday Bus Stop Boardings in October 2012 — Chicago
- Bus Stop — Baton Rouge
- Everett Transit - Bus Stop Utilization — Everett


**street name** — 4 datasets across 4 cities

- Street Name Signs Work Orders (Historical) — New York
- 911 Addressing - Street Name Master List — Austin
- EBRP Street Name Changes — Baton Rouge
- Street Name — New Orleans


**council district** — 4 datasets across 4 cities

- Zone Updates And Staff Comments Per Council District — Austin
- Parking Occupancy Tax Business Locations within Council District 13 — Los Angeles
- Council District — Oakland
- Zachary Council District — Baton Rouge



## The same tail, clustered by embedding

A second view, kept because it groups datasets that share no vocabulary. k-means returns *k* clusters whether or not *k* themes exist, so each carries its **coherence** — the mean cosine of its members to its own centroid. Below 0.62, a cluster is a partition rather than a theme and is marked diffuse; **17 of 40 are.** Read those as noise, not as findings.

| Coherence | Cities | Datasets | Terms | Closest SDG indicator |
|---:|---:|---:|---|---|
| 0.992 | 3 | 231 | dfs, check, speed, sign | Beach litter items per unit of surface area  |
| 0.839 | 5 | 70 | libraries, location, holds | Countries with users/communities participati |
| 0.81 | 6 | 42 | foia, request, log | Countries that have legislative, administrat |
| 0.766 | 2 | 50 | repave, miles, arterials, arterial, lane | Number of deaths rate due to road traffic in |
| 0.742 | 7 | 44 | insight, edmonton, survey, community | Participation rate in organized learning (on |
| 0.713 | 24 | 159 | (no term covers a fifth of this cluster) | Land area |
| 0.707 | 10 | 57 | election, voting, general, results | Number of local governments |
| 0.702 | 23 | 151 | (no term covers a fifth of this cluster) | Countries that have national urban policies  |
| 0.692 | 19 | 92 | (no term covers a fifth of this cluster) | Number of deaths rate due to road traffic in |
| 0.687 | 2 | 32 | optimized, corridors, timing, signal | Progress toward productive and sustainable a |
| 0.673 | 19 | 128 | (no term covers a fifth of this cluster) | Land area |
| 0.672 | 13 | 56 | (no term covers a fifth of this cluster) | Number of deaths rate due to road traffic in |
| 0.662 | 3 | 100 | des | Coastal Eutrophication: Total Nitrogen (micr |
| 0.661 | 16 | 99 | school | Extent to which global citizenship education |
| 0.658 | 21 | 90 | (no term covers a fifth of this cluster) | Countries that adopt and implement constitut |
| 0.654 | 17 | 72 | (no term covers a fifth of this cluster) | Number of local governments |
| 0.654 | 6 | 51 | edmonton | Countries that have national urban policies  |
| 0.654 | 4 | 63 | stairway, sidewalks | Number of deaths rate due to road traffic in |
| 0.64 | 22 | 141 | (no term covers a fifth of this cluster) | Number of deaths rate due to road traffic in |
| 0.64 | 15 | 81 | (no term covers a fifth of this cluster) | Countries that adopt and implement constitut |
| 0.638 | 20 | 88 | (no term covers a fifth of this cluster) | Net inbound official development assistance  |
| 0.629 | 19 | 78 | bike, parking | Number of deaths rate due to road traffic in |
| 0.622 | 6 | 19 | covid- | Number of total conflict-related deaths |
| 0.62 *(diffuse)* | 16 | 42 | csb, update, response, time | Police reporting rate for robbery in the pre |
| 0.619 *(diffuse)* | 18 | 67 | (no term covers a fifth of this cluster) | Countries with users/communities participati |
| 0.619 *(diffuse)* | 13 | 41 | ems, calls | Number of deaths due to disaster |
| 0.611 *(diffuse)* | 17 | 57 | neighborhood, street | Number of deaths rate due to road traffic in |
| 0.611 *(diffuse)* | 14 | 43 | sweeping, schedule, street | Countries with procedures in law or policy f |
| 0.608 *(diffuse)* | 8 | 25 | beudo, engagement, employee, buildings | International financial flows to developing  |
| 0.605 *(diffuse)* | 20 | 67 | (no term covers a fifth of this cluster) | Land area |
| 0.601 *(diffuse)* | 7 | 55 | school | Adjusted gender parity index for participati |
| 0.6 *(diffuse)* | 10 | 21 | (no term covers a fifth of this cluster) | Beach litter items per unit of surface area  |
| 0.6 *(diffuse)* | 7 | 43 | (no term covers a fifth of this cluster) | Score of adoption and implementation of nati |
| 0.598 *(diffuse)* | 17 | 36 | analytics | Proportion of results indicators drawn from  |
| 0.597 *(diffuse)* | 26 | 88 | permits, building | Countries with procedures in law or policy f |
| 0.593 *(diffuse)* | 9 | 40 | storm | Total inbound official flows for infrastruct |
| 0.58 *(diffuse)* | 14 | 59 | employee | Total government revenue, in local currency |
| 0.514 *(diffuse)* | 16 | 47 | (no term covers a fifth of this cluster) | Countries with integrated biodiversity value |
| 0.513 *(diffuse)* | 13 | 35 | library, austin | Total inbound official flows for infrastruct |
| 0.481 *(diffuse)* | 11 | 26 | (no term covers a fifth of this cluster) | Countries that have legislative, administrat |

### The coherent clusters in detail

**dfs, check, speed, sign** — 231 datasets across 3 cities (coherence 0.992, mean affinity 0.323)

*Most central to the cluster:*

- Speed Check Sign - DFS007 — Edmonton
- Speed Check Sign - DFS003 — Edmonton
- Speed Check Sign - DFS190 — Edmonton
- Speed Check Sign - DFS170 — Edmonton
- Speed Check Sign - DFS002 — Edmonton


*One per city, to show the spread:*

- Speed Check Sign - DFS041 — Edmonton
- Speed Limits — Calgary
- Real-Time Midblock Traffic Data — Winnipeg
- Mobile Automated Photo Enforcement Ticket Zones — Edmonton
- Speed Check Sign - DFS001 — Edmonton


**libraries, location, holds** — 70 datasets across 5 cities (coherence 0.839, mean affinity 0.324)

*Most central to the cluster:*

- Libraries - 2019 Holds Filled by Location — Chicago
- Libraries - 2012 Holds Filled by Location — Chicago
- Libraries - 2011 Holds Filled by Location — Chicago
- Libraries - 2014 Holds Filled by Location — Chicago
- Libraries - 2013 Holds Filled by Location — Chicago


*One per city, to show the spread:*

- Libraries - 2014 Visitors by Location — Chicago
- Average Discount per Customer FY 2024 — Austin
- Discrimination Case Closures by Month and Type, 2017-Present — Seattle
- T10 Bus Travel Time — Santa Monica
- Summer of 2014, Weekly Camp, Pool and Water Park Attendance — Providence


**foia, request, log** — 42 datasets across 6 cities (coherence 0.81, mean affinity 0.335)

*Most central to the cluster:*

- FOIA Request Log - Transportation — Chicago
- FOIA Request Log - Buildings — Chicago
- FOIA Request Log - Fire — Chicago
- FOIA Request Log - Law — Chicago
- FOIA Request Log - City Clerk — Chicago


*One per city, to show the spread:*

- 311 Call Center Inquiry — New York
- Memos to Council — Edmonton
- FOIA Request Log - Police — Chicago
- Community PC Program_Number of Devices — Austin
- COBAN Logs — Seattle


**repave, miles, arterials, arterial, lane** — 50 datasets across 2 cities (coherence 0.766, mean affinity 0.25)

*Most central to the cluster:*

- 9 - Repave 180 Miles Of Arterials-3 — Seattle
- 9 - Repave 180 Miles Of Arterials — Seattle
- Lane Miles Repaved 2020 Q2 — Seattle
- 2 - Repave 180 Miles Of Arterials (2016 Final) — Seattle
- 9 - Repave 180 Miles Of Arterials2018-3 — Seattle


*One per city, to show the spread:*

- 20 - Miles of ITS 2020 Q3 — Seattle
- Lane Miles Resurfaced Year to Date — Roseville
- MS4 Miles Swept 2014 — Seattle
- AMM Widgets-2 — Seattle
- Arterial Lane Miles Re-Striped — Seattle


**insight, edmonton, survey, community** — 44 datasets across 7 cities (coherence 0.742, mean affinity 0.334)

*Most central to the cluster:*

- Planning A Day At An Attraction - Edmonton Insight Community — Edmonton
- Community Recreation Facilities - Edmonton Insight Community — Edmonton
- Transit - Edmonton Insight Community — Edmonton
- December 2022 Mixed Topic - Vehicle for Hire - Edmonton Insight Community — Edmonton
- Waste Drop-off - Edmonton Insight Community — Edmonton


*One per city, to show the spread:*

- Directory Of Family Shelter Performance Ranking FY 2012 Q4 and 2013 Q1 — New York
- Licensed Cabs ID And Safety - Edmonton Insight Community — Edmonton
- EMS - Ambulance Responses by Month — Austin
- Citizen Satisfaction Survey (2016-2017) — Calgary
- Community Survey 2014 — Dallas


**(no term covers a fifth of this cluster)** — 159 datasets across 24 cities (coherence 0.713, mean affinity 0.338)

*Most central to the cluster:*

- 311 Service Requests - Street Lights - All Out - Historical — Chicago
- Speed Camera Violations — Chicago
- 311 Service Requests - Alley Lights Out - Historical — Chicago
- Bike Fix It Stations — Austin
- 311 Service Requests - Tree Trims - Historical — Chicago


*One per city, to show the spread:*

- Mobile Telecommunications Franchise Pole Reservation Locations — New York
- Rainfall History - (2013 - 2015) — Edmonton
- 311 Service Requests - Vacant and Abandoned Buildings Reported - Historical — Chicago
- Austin MetroBike Kiosk Locations — Austin
- Calgary Public Library Locations and Hours — Calgary


**election, voting, general, results** — 57 datasets across 10 cities (coherence 0.707, mean affinity 0.321)

*Most central to the cluster:*

- 2013 Election Results by Voting Station — Calgary
- 2017 Official Election Results by Voting Station — Calgary
- 2017 Official Election Results (by Voting Station) — Edmonton
- Official Results - General Election 2021 - Senate — Calgary
- Official Results - General Election 2021 — Calgary


*One per city, to show the spread:*

- Voting/Poll Sites — New York
- 2013 Edmonton Election - Results Details (by Voting Station) — Edmonton
- 7th Ward Alderman Applicants - 2013 — Chicago
- Council and Committee Votes — Calgary
- Election 2015 May General Voting Results — Los Angeles


**(no term covers a fifth of this cluster)** — 151 datasets across 23 cities (coherence 0.702, mean affinity 0.321)

*Most central to the cluster:*

- City_Limits — Oakland
- Neighborhood Improvement District — Kansas City
- neighborhoods — Oakland
- Community Improvement District — Kansas City
- School Districts — Kansas City


*One per city, to show the spread:*

- DSNY Frequencies — New York
- Contour Lines LL - WGS84 — Edmonton
- Census Blocks — Chicago
- railroads — Austin
- 3D Buildings - Citywide — Calgary


**(no term covers a fifth of this cluster)** — 92 datasets across 19 cities (coherence 0.692, mean affinity 0.327)

*Most central to the cluster:*

- Street Centerline — Austin
- Moving Container or Crate parking permit — Cambridge
- Special Event Parking Permits — Cambridge
- TRANSPORTATION.pw_current_yr_service_plan — Austin
- Sidewalks — Austin


*One per city, to show the spread:*

- Street Closures due to Construction Activities by Block — New York
- Residential Street Cleaning Schedule — Edmonton
- Winter Overnight Parking Restrictions — Chicago
- Sidewalks — Austin
- On-Street Parking Zones — Calgary


**optimized, corridors, timing, signal** — 32 datasets across 2 cities (coherence 0.687, mean affinity 0.265)

*Most central to the cluster:*

- Corridors With Optimal Signal Timing-2 — Seattle
- 4D - Corridors Optimized with Signal Timing 2019 — Seattle
- 4D - Corridors with Optimized Signal Timing Q32019 — Seattle
- 4D - Corridors with Optimized Signal Timing 2019 Final — Seattle
- Corridors Optimized 2020 Q2 — Seattle


*One per city, to show the spread:*

- OW Metrics Marion-2 — Seattle
- Traffic Signal Audits — Mesa
- Corridors With Optimal Signal Timing-2 — Seattle
- Q1 2015 Initial Update For New Electric Vehicle Miles Goal — Seattle
- Copy Of Q1 2015 Initial Update For New Electric Vehicle Miles Goal — Seattle



## Reproducing

```bash
python3 probe/fetch_municipal.py
python3 probe/inverse.py
```

