---
layout: default
title: "Crosswalk at 11 pairs: only 3 can honestly share an axis"
author: Devin
date: 2026-09-14 23:00:00 -0400
---

Expanded the crosswalk from 3 pairs to 11. Three are chartable. That ratio is the finding.

| Pair | SDG | Tier | Grade | Chartable |
|---|---|---|---|---|
| PM2.5 annual mean | 11.6.2 | 1 | PROXY | **yes** |
| Intentional homicide | 16.1.1 | 3 | PROXY | **yes** |
| Municipal waste recycled | 11.6.1 | 3 | PROXY | **yes** |
| Road traffic deaths | 3.6.1 | 3 | BLOCKED | no |
| Child mortality | 3.2.1 | 3 | CONTEXT | no |
| Maternal mortality | 3.1.1 | 3 | BLOCKED | no |
| Deaths from air pollution | 3.9.1 | 3 | CONTEXT | no |
| Poverty | 1.2.1 | 3 | CONTEXT | no |
| Inadequate housing | 11.1.1 | 2 | CONTEXT | no |
| Built-up area per capita | 11.7.1 | 1 | NO-NYC-SOURCE | no |
| Safely managed drinking water | 6.1.1 | 3 | NO-SIGNAL | no |

## The harness had the exact bug we are building against

First run reported **BLOCKED and CONTEXT pairs as "chartable: yes"**. The mechanical checks —
does it resolve, do units agree, is there overlap — all passed, so the probe waved them through
over the top of a human judgment that said these must not share an axis.

Road traffic deaths was the clearest case: marked chartable on a **single** overlapping year.

Fixed two ways. The human grade now **vetoes** the mechanical result, and a trend needs at least
five overlapping years rather than a shared endpoint. Worth dwelling on, because it is the
product's whole thesis reproduced in our own tooling: every automated check passed, and the
answer was still wrong. Units agreeing is necessary and nowhere near sufficient.

## Why the eight fail, which is the interesting part

- **Age bands** — UN counts child deaths under five, NYC's series is under one. Both are raw
  counts, so units "agree". A chart would look perfect and compare different populations.
- **Denominators** — maternal mortality is per 100,000 **live births**, not per population, and
  NYC's births live in a different dataset. Also NYC publishes pregnancy-*associated* deaths, a
  deliberately broader definition.
- **Concept** — the UN poverty series is the **international** extreme-poverty line (~$2.15/day).
  For any US city that is near zero and carries no signal. NYC's own measure is an order of
  magnitude higher. Two numbers sharing a name and measuring nothing alike.
- **Measure type** — UN reports the *share of urban population* in inadequate housing; NYC's
  nearest analogue is a *count* of hazardous housing violations, which tracks inspection activity
  as much as conditions.
- **No NYC source** — built-up area per capita has Tier 1 UN data with city-level slices across
  countries, and no NYC equivalent found yet.
- **Ceiling effect** — safely managed drinking water sits at ~100% for the US and would for NYC.
  Two flat lines at 100 tell an analyst nothing. Excluded deliberately, and written down as such.

## The inversion worth showing at the event

**Road traffic deaths is blocked by the UN side, not by us.** NYC has Vision Zero collision data
updated daily, every fatality geocoded. The UN has one modelled estimate from 2021. For the
city's flagship street-safety programme, the international comparison simply does not exist.

That is the argument for city data flowing *toward* the UN system rather than only the reverse,
and it is a better conversation to have with UNSD in the room than another dashboard.
