---
layout: default
title: "The inverse crosswalk: what cities measure that the SDGs do not"
author: Devin Balkind
date: 2026-09-16 21:05:00 -0400
---

Every analysis in this repo has run city → UN: take an SDG indicator, find the municipal dataset
that matches it. That direction can only ever discover what the framework already asks about. So:
run it backwards. Take **11,206 datasets from 37 city portals**, find each one's nearest neighbour
among **all 689 SDG indicators**, and look at what is left over.

The question is not which cities are behind. It is **what would SDG 11 look like if it had been
written from municipal data upward?**

[Full results](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-latest) ·
`python3 probe/inverse.py`

## The answer, as far as it goes

Themes that recur across many independent city catalogs and sit in the bottom quartile of every
one of them:

| Cities | Theme |
|---:|---|
| 23 | Building permits, licences and code enforcement |
| 15 | **Records-access request logs** (FOIA and equivalents) |
| 13 | Bike parking, bike share, active-travel space |
| 10 | Street sweeping schedules and parking enforcement |
| 10 | **Call-centre response performance** — answer times, 311 service levels |
| 9 | Pedestrian and bicycle counts |
| 8 | Property sales and assessment |
| 7 | For-hire vehicle and taxi trip records |
| 7 | Fire stations and emergency facilities |
| 6 | Special events permitting |

**The sharpest one is records access.** Fifteen cities publish request logs — how many were filed,
how many answered, how long it took. The nearest SDG indicator the matcher can find is 16.10.2,
*"countries that adopt and implement constitutional, statutory and/or policy guarantees for public
access to information."* The framework asks **whether a law exists**. The cities publish
**whether the law works**. A country can score full marks on 16.10.2 and answer nothing, and no
indicator in the framework would notice.

The same shape appears in call-centre performance: the SDGs have no concept of *how quickly a
government responds to its residents*, and ten cities publish exactly that, in seconds.

## The other direction

**123 of the 689 indicators were the nearest neighbour of no municipal dataset at all.** Many are
honestly national — ODA flows, external debt, climate finance, which no city could report. But the
list also contains **e-waste collected, generated and recycled per capita**, and **hazardous waste
generated** — which is a double gap. Those are the same indicators we found the United States does
not report, and it turns out cities do not publish them either. Nobody is measuring them at any
level of government.

## What this is worth, stated honestly

**One positive control in seven failed.** NYC's *Housing Maintenance Code Violations* is a
hand-verified match for SDG 11.1.1 inadequate housing, and it landed at the 24th percentile —
inside the tail. So the tail contains real matches, and any individual dataset in it may simply
have been missed. That is why the unit of evidence above is *cities*, not datasets: one dataset
scoring low is retrieval failure, and twenty cities independently publishing the same category is
not.

**Fourteen of forty clusters are noise**, and the report says which. k-means returns *k* clusters
whether or not *k* themes exist; each one now carries the mean cosine of its members to its own
centroid, and below 0.62 it is published as *diffuse* rather than read as a theme. The first run
had no such measure and cheerfully labelled a cluster "school" that contained building violations
and lobbyist registrations.

**English-language portals only.** Comparing cosine similarities across two embedding models is
meaningless, so the multilingual catalogs need their own run.

## The bug underneath it

The first run's clusters were incoherent, and the reason was not the clustering.

`embed.Index` decided whether cached vectors could be reused by checking **`len(cached_ids) ==
len(datasets)`**. Re-fetch a portal months later and it returns the same datasets in a *different
order* — measured: **24 of 45 city catalogs did exactly that**. Same count, same IDs, different
sequence. The length check accepted it, and every dataset was handed another dataset's vector.

There is no symptom. Similarity scores stay in range, rankings look ordinary, nothing errors. It
surfaced only because a cluster labelled "school" was full of facade-compliance filings and I
looked at the rows.

It now matches on IDs, and when the set is identical but re-ordered it permutes the cached vectors
instead of re-embedding. Worth noting what this *didn't* affect: the published municipal table was
computed on the run that created its cache, in the order it created it, so those numbers were
right. The bug only bites on a later re-run — which is to say, it was waiting for the next person
to re-render the table.

That is the eighth entry in this project's list of automated checks that produced a confident
wrong answer, and the fourth caught by reading rows rather than totals.
