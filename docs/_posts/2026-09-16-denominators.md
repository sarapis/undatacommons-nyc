---
layout: default
title: "Denominators: Eurostat is the obvious answer and it is wrong"
author: Devin
date: 2026-09-16 18:00:00 -0400
---

Most SDG indicators are rates per 100,000, so every non-US city needs a population figure before
it can produce a chart. Two are now wired, and the route we did not take is the more useful
finding.

## Eurostat's Urban Audit publishes greater cities

`urb_cpop1` covers 969 European cities annually and is exactly the single source this needs. It
reports **greater cities**, not municipalities:

| City | Eurostat "greater city" | Municipality | If used |
|---|---:|---:|---|
| Madrid | 5,115,272 | **3,520,396** | rates ~31% too low |
| Milan | 3,580,530 | **1,399,079** | rates ~60% too low |

For Madrid the table contains *no municipality entry at all* — the greater city is the only
option. A city's open data covers its municipality, so this is the denominator mismatch the whole
project exists to catch, and it would have been completely invisible in the output.

## So denominators come from the cities themselves

Better provenance as well: numerator and denominator then share a publisher.

**Madrid** — *Padrón municipal* (`200076-0-padron`), summing the four Spanish/foreign ×
male/female columns of a 34 MB CSV: **3,520,396** as of 2026-09-01. A snapshot, so Madrid supports
levels and not trends until the historic padrón is wired.

**Milan** — *Popolazione calcolata* (`ds1494`), year-end population **1880–2025**, ISTAT to 2002
then the city's own anagrafe: **1,399,079** in 2025. A series, so Milan supports **trends** — the
first non-US city that does.

Two cities, two shapes, two resolvers. City statistical publications do not share a format, and
pretending otherwise is how you end up with Eurostat.

## The bug this work exposed

Building a summary table showed **Chicago and Boston both reporting 8,478,072** — New York's
population.

The census resolver fell through to NYC's place code whenever a city declared none of its own.
Chicago's registry entry named its place code in a prose `source` string but carried no structured
field, so it silently inherited NYC's 8.5 million. **Every Chicago rate would have been three
times too low, and nothing in the output would have looked wrong.**

There is now no fallback. A city using the census module without explicit state and place FIPS
raises, with the reason: *refusing to guess, a wrong denominator is invisible in the output.*

That is the fifth automated path on this project that produced a confident wrong answer, and the
second where the failure mode was a silent default rather than an error.

## Where it stands

| City | 2023 population | Source |
|---|---:|---|
| New York | 8,258,035 | Census ACS |
| Madrid | 3,520,396 | Padrón municipal |
| Chicago | 2,664,454 | Census ACS |
| Milan | 1,417,597 | Popolazione calcolata |
| San José | 969,615 | Census ACS |
| Boston | 652,442 | Census ACS |

Plus 23 more US cities resolvable by ACS place code. Buenos Aires declares no source and is
refused rather than estimated. **24 non-US cities still need one**, and each needs a person to
find its statistical publication — the part that does not automate.
