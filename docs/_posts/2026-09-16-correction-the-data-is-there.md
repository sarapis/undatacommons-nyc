---
layout: default
title: "Correction: the other cities do have comparable data — our matcher just can't find it"
author: Devin
date: 2026-09-16 12:00:00 -0400
---

The briefing and the last two posts carried this line:

> No substantive SDG indicator has matched outside NYC.

True of our matcher. **Read as a statement about the cities, it is wrong**, and it was phrased so
it would be read that way. Correcting it.

## The data is there

Searching Chicago's and Boston's catalogs directly, by hand, for the four indicators NYC is
crosswalked on:

| | Chicago (915 datasets) | Boston (235) |
|---|---|---|
| Crime / homicide | **Crimes — 2001 to Present** | Shootings · Homicide Clearance Rate |
| Road deaths | **Traffic Crashes — Crashes / People** | **Vision Zero Fatality Records** |
| Air quality | **Open Air Chicago** (measurements, hourly, daily) | only building emissions (BERDO) |
| Waste | Christmas tree recycling; no municipal tonnage | Trash *schedules*, not tonnage |

Chicago's *Traffic Crashes — Crashes* is structurally the same thing as the NYC dataset behind our
road-deaths card. Boston publishes a dataset literally called **Vision Zero Fatality Records** —
the same programme, the same concept, named almost identically to what we used for NYC.

## What our matcher did with it

Querying Boston for *"Death rate due to road traffic injuries"*:

```
0.486  Traffic-Related Data
0.467  City of Boston Contract Award
0.444  My Neighborhood Dataset
0.387  Trash Collection Days
...
#23    Vision Zero Fatality Records        (0.286)
```

**The correct dataset ranked 23rd of 235, below a contract-award file.** No threshold rescues
that; it is a retrieval failure, not a calibration one.

The matcher is not uniformly blind — querying homicide returns *Homicide Clearance Rate* at rank 1,
because the word "homicide" appears in the title. It works when the vocabulary happens to line up
and fails when a city names the same concept differently, which cities routinely do. "Vision Zero"
is a programme name, not a description of its contents.

## The honest position

- **Chicago and Boston hold data comparable to what NYC is crosswalked on.** Air quality in
  Chicago, road fatalities in both, crime in both.
- **Some gaps are real.** Neither publishes municipal waste tonnage in the DSNY sense, and
  Boston's only air dataset is building emissions rather than ambient concentrations.
- **Our matcher cannot find what is there.** That was already the stated conclusion — "nothing
  shows the matcher can lead" — but stating it alongside "no indicator matched outside NYC"
  implied the cities were empty. They are not.

This is the third time on this project that an automated check produced a confident answer a
person overturns by reading for five minutes: the chartable flag that ignored human grades, the
screen that reported 689 having recorded 9, and now a matcher whose silence was mistaken for
absence.

**A null result from a tool you have measured at ~50% precision is not evidence of absence.** We
wrote that lesson into the spec as R1 and then made the mistake anyway, in our own prose, about
our own tool.
