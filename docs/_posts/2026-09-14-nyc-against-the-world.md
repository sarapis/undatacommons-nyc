---
layout: default
title: "NYC against the world, not just the US — and the homicide result inverts"
author: Devin
date: 2026-09-14 23:30:00 -0400
---

Every chart in the demo compared NYC to the United States. That was a limit of my framing, not of
the data: `get_child_observations` over `Earth` / `Country` returns **every reporting country in
one call**, and the response carries `entityMetadata` names, so no separate lookup is needed.

Each card now shows where NYC sits among all reporting countries in **2019**.

| Indicator | NYC | Rank | Nearest neighbours |
|---|---:|---:|---|
| PM2.5 (city aggregates) | 6.60 µg/m³ | **#5 of 186** | Finland, Estonia, Iceland |
| Homicide | 3.63 per 100k | **#85 of 137** | Pakistan, Montenegro |
| Waste recycled | 17.3% | **#38 of 64** | Bahrain, Greece |

## The homicide result inverts the story

Against the United States, NYC crossed below the national rate in 2013 and stayed below — a
success story, and the one we put on the chart yesterday.

Against the world, NYC sits in the **bottom half**, 85th of 137, between Pakistan and Montenegro,
with 84 countries reporting a lower rate.

**Same number. Different comparator. Opposite conclusion.** Neither is wrong. A tool that shows
only the first is not neutral — it is flattering, and it is flattering by omission. This is the
definitional-caveat lesson again, arriving through a different door: the choice of *who you
compare to* is as load-bearing as what you measure.

Tier still governs. PM2.5 is Tier 1, so NYC is measured against other countries' **city
aggregates** — genuinely like-for-like. Homicide and waste are Tier 3: a city against whole
nations, which is real context and not a peer comparison, since cities generally run above their
national averages.

## One year, deliberately

`date: "latest"` returns each country's *own* latest vintage — Afghanistan 2023 sitting beside
Aruba 2014. That is precisely the mixed-vintage comparison this project exists to catch, so
everything is pinned to 2019, the last year with wide coverage across all three.

## An impossible number in the authoritative data

**Malaysia reports 147.7% of its municipal waste recycled in 2019.** You cannot recycle more
waste than exists. It is in the UN SDG database, and one bad figure was flattening the entire
distribution on the chart.

We clipped it off the axis, drew it in red at the edge, kept it in the data and named it in the
caption. Deleting it would have produced a cleaner chart and a dishonest one — a silent drop is
how a dataset launders its own errors. Two countries also return empty names from
`entityMetadata`; those fall back to their ISO codes rather than rendering blank.

For a room asked *how do you hold the line on truth in a world flooded with synthetic data*, a
demonstrably impossible figure sitting in authoritative UN statistics is a more useful exhibit
than anything we could have contrived.
