---
layout: default
title: "What NYC can say that the United States cannot"
author: Devin Balkind
date: 2026-09-17 11:20:00 -0400
---

The asymmetry this project keeps circling: the UN graph is national-level, so a city can only be
placed against countries — and for **130 of the 442 usable SDG indicators the United States
reports nothing at all**. On those, *NYC vs the US* is not a weaker comparison than *NYC vs the
world*. It is the only one available, and the US is not in it.

Built the worksheet:
[`us-silent-latest`](https://sarapis.github.io/undatacommons-nyc/artifacts/us-silent-latest) ·
`python3 probe/us_silent.py`

## The number is 39, not 67

The briefing has said **67** since the corpus was first screened — 130 US-silent indicators, of
which the scope classifier judged 67 city-scoped. Building the worksheet showed that number is
inflated, and why.

**28 of the 67 have a country as their subject, not a place.** *"Extent to which countries have
laws and regulations that guarantee full and equal access to sexual and reproductive health care"*
is not a quantity New York City can hold a value for; the question is whether a national
legislature passed something. Eighteen of the 28 are that one family — the SDG 5.6.2 legal
provisions — and the matcher paired **every one of them** with NYC's *Local Law 37/2011 Temporary
Housing Assistance*, on the token "Law".

The scope classifier could not have caught this. It reads an indicator's *topic* — health, water,
education — and judges it municipal, which for 5.6.2 it is. What it cannot see is that the
sentence measures a legislature. So that filter is now a lexical rule rather than a classifier:
*"extent to which…", "countries that…", "proportion of countries…"* are excluded, and *"extent
of human made wetlands"* is not. A rule you can read and argue with beats a score you cannot.

**39 survive.** 38 have a peer group of 15+ reporting countries, and 26 also have an NYC candidate
above the noise floor.

## The real answer is waste and water

Twelve of the 39 form one coherent group, and it is the group the briefing predicted:

| Countries | Indicator | Years | NYC candidate |
|---:|---|---|---|
| 133 | Municipal waste collected | 2000–2023 | Recycling Diversion and Capture Rates (0.63) |
| 107 | Hazardous waste generated per unit of GDP | 2000–2024 | Wastewater Co-digestion and Biogas (0.53) |
| 97 | Hazardous waste exported | 2000–2024 | DSNY Disposal Sites Used by Facilities (0.52) |
| 97 | Total waste generation | 2000–2023 | DSNY Waste Characterization (0.52) |
| 94 | Total wastewater treated | **2022 only** | Watershed Water Quality – Wastewater (0.54) |
| 93 | Hazardous waste treated or disposed | 2000–2024 | Dewatered Solids and Biosolids (0.51) |
| 88 | Proportion of hazardous waste treated or disposed | 2000–2024 | Dewatered Solids and Biosolids (0.51) |
| 85 | Hazardous waste imported | 2000–2024 | DSNY Disposal Sites Used by Facilities (0.49) |
| 84 | Groundwater bodies with good ambient water quality | 2017–2023 | Watershed Water Quality – Limnology (0.52) |
| 84 | Total wastewater generated | **2022 only** | Wastewater Co-digestion and Biogas (0.59) |
| 72 | Proportion of wastewater treated | **2022 only** | Dewatered Solids and Biosolids (0.52) |
| 55 | Extent of human made wetlands | 2021–2025 | NYC Wetlands (0.50) |

These are DSNY and DEP series. NYC genuinely publishes them, and **133 countries report municipal
waste collected while the United States reports none of it.** That is a comparison NYC can make and
its own country cannot.

Three of the twelve carry **one year**. That supports a level comparison and not a trend — the same
finding that removed road safety as our headline demo, and the worksheet marks it rather than
letting a reviewer discover it after choosing the indicator.

## What corroborates it

Two results from the last two days point at the same set from opposite directions.

The [corpus smell test](https://sarapis.github.io/undatacommons-nyc/artifacts/smell-latest) found
that sweeping all 689 indicators rather than the 442 usable ones adds almost nothing — **but the 40
that do hold data are almost entirely e-waste and municipal waste import/export**.

The [inverse crosswalk](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-latest) found
**e-waste and hazardous waste per capita among the 123 indicators no municipal dataset comes near**
— nobody publishes them at city level either.

So this band of the framework is thinly reported by everyone: the US skips it, cities mostly skip
it, and it is exactly where a city that *does* publish has something unusual to say.

## The screen held

`screen.py` decides *does the US report this* from `entityCoverage` on a six-country panel — a
proxy we have flagged as a proxy. Checked all 39 against the actual country observations:
**not one has a single United States datapoint.** The proxy and the data agree completely.

That is the second independent confirmation of that panel this week; yesterday's `--all` sweep
showed its `NO-DATA` grade predicts global emptiness 84% of the time.

## Where it is still weak

- **12 of the 39 have no candidate above 0.45**, the floor below which a proposal is noise. They
  are listed with the candidate in italics rather than silently dropped.
- Some above the floor are still wrong. *Malaria incidence per 1,000 population at risk* →
  *Projected Population 2010–2040* at 0.48 is a false match, and NYC has no malaria.
- **It is a worksheet, not a crosswalk.** Under spec v0.1 a grade is a human judgment, so every
  row is `graded: false`. Nothing here is a mapping until a person says it is.

## Also today

The platform went fully public this morning. `python3 probe/launch_diff.py`: **57 series, 12
variables and 689 corpus indicators, zero drift** against yesterday's pre-launch baseline, and
`mcp/smoke.py` 8/8. No public hostname resolves yet — `undatacommons.unicc.biz` and
`datacommons.un.org` both still refuse — and the deployment we have always used is still answering.
The demo is safe.
