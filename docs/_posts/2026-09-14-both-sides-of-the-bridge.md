---
layout: default
title: "DOU_CITY recovers peer comparison, and the NYC half is messier than the UN half"
author: Devin
date: 2026-09-14 17:30:00 -0400
---

Two probes done. One unblocks the open decision; the other says the NYC side needs the same
rigour we gave the UN side.

## The peer-comparator question has a third answer

`URBANIZATION--DOU_CITY` is a real population-weighted aggregate, not a token. For the US it
covers 121M of 347M people, and the city figure differs meaningfully from the national one
(PM2.5 2019: 7.57 city vs 7.18 national).

The important part: **it exists for other countries too, with full 10-year series.** PM2.5 city
aggregate, 2019 — US 7.57, Canada 6.87, UK 10.06, Japan 11.32, Germany 11.92, France 12.03,
Colombia 15.97, Mexico 19.04.

So we can compare NYC against *the city aggregate of other countries* using nothing but UN Data
Commons — one source, one method, one unit, consistent DEGURBA definitions. That is arguably
**better** than the NYC-vs-London comparison we originally promised: no cherry-picked comparator,
no second source to reconcile. Recommending this as the primary framing.

Caveat to state on any such chart: NYC is itself inside the US city aggregate (~7% of it).

## The NYC half needed the same treatment

Built a pair probe that verifies *both* sides of every crosswalk entry. It immediately found
things a human eye would have missed:

- **NYPD complaint data carries junk pre-2006 incident dates** — 17 murders in 1990, when the
  real figure was over 2,000. Filtering to 2006+ gives the true series (569 in 2006 → 277 in
  2025).
- **PM2.5 has summer/winter rows alongside the annual mean.** Query the obvious way and you
  silently average three different measures together.
- **DSNY's `month` field is text** (`"2026 / 08"`), so `date_extract_y` fails outright — and
  rows before 1993 predate curbside recycling entirely.
- The published *Recycling Diversion and Capture Rates* dataset **has not updated since 2020**;
  the live path is deriving the rate from monthly tonnage.

Two of three pairs now resolve end to end. Homicide is blocked: NYC publishes a count, the UN
publishes a rate per 100,000, and the Census ACS denominator now needs a free API key.

## What the numbers say

**PM2.5** — NYC is *below* the US city average and the gap is widening: 8.93 vs 9.23 in 2014,
6.60 vs 7.57 in 2019.

**Waste recycling** — NYC at 17.2% against 23.6% for the US in 2018. But NYC's figure is DSNY
residential collection only, while the UN municipal-waste definition includes commercial. **The
gap is probably overstated, and the honest answer is that these are not measuring the same
universe.**

That contrast is the demo. One indicator where NYC looks good, one where it looks bad, and the
bad one carries a caveat that changes the interpretation. It is the argument for the whole
project in two charts.

[Crosswalk status](https://sarapis.github.io/undatacommons-nyc/artifacts/crosswalk-latest) ·
`python3 probe/pair_probe.py`
