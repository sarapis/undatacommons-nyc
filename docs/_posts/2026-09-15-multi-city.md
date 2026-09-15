---
layout: default
title: "Multi-city: the plumbing generalises, the matching does not"
author: Devin
date: 2026-09-15 22:00:00 -0400
---

Generalised the pipeline to any city, over Socrata **or** CKAN, and ran it against five. The
infrastructure works. The recommender does not travel, and that is the useful result.

| City | Platform | Lang | Datasets | Field names | Candidates | Best sim |
|---|---|---|---:|---:|---:|---:|
| Chicago | socrata | en | 915 | 915 | 6 | 0.55 |
| Boston | ckan | en | 235 | 0 | 7 | 0.57 |
| San José | ckan | en | 170 | 0 | 4 | 0.58 |
| Madrid | ckan | es | 672 | 0 | **0** | 0.27 |
| Milan | ckan | it | 2602 | 0 | **0** | 0.29 |
| Buenos Aires | ckan | es | — | — | — | portal dropped the connection |

## Cross-language matching fails outright

Not degradation. Madrid tops out at **0.265** and Milan at **0.294** against Boston's 0.575,
with medians around 0.15 — noise. **Milan has a larger catalog than NYC and matches nothing.**

Lowering the threshold would admit garbage rather than signal: Madrid's best single match pairs
*carbon dioxide emissions per unit of GDP* with *municipal parking permit lists*. The embedding
model is English-only and no amount of tuning fixes that.

Since most VLR cities are not anglophone, this is the blocker for the whole multi-city idea.

## We were wrong about field names

Last note predicted CKAN cities would be handicapped because CKAN does not publish column names
and Socrata does — columns being what moved NYC's waste pair from rank 882 to 23.

**Chicago publishes field names on 915 of 915 datasets and found *fewer* candidates than Boston,
which publishes none.** Hypothesis dead. Recording it because a prediction that survives only
until it is tested is worth more written down than quietly dropped.

## The threshold does not transfer between catalogs

0.50 was calibrated on NYC's 2,400-dataset catalog. In a smaller catalog the nearest neighbour is
whatever is least unrelated, so the same number now admits nonsense — Boston's top match pairs
*Food waste* with *Trash Schedules by Address* at 0.57.

Reading all 13 English-city candidates by hand: roughly **2–3 per city are plausible**, and **no
substantive SDG indicator matched in any city.** No air quality, no homicide, no waste tonnage, no
road deaths. What matched was generic budget, land and performance vocabulary sharing words with
indicator names.

An absolute cosine score has no fixed meaning across catalogs. It needs to be a percentile, or a
margin over that catalog's own distribution.

## One constraint that fell out of the spec

The bootstrapper **cannot** emit a crosswalk. Spec v0.1 makes a grade a human judgment, so a
machine producing one would violate the spec this project just published. Output is
`candidates.json` with `is_crosswalk: false` — the worksheet a local analyst grades.

That constraint was not designed in; it fell out of the spec, which is a sign the spec is doing
real work rather than describing what we already did.

## Where that leaves it

NYC's good pairs were found by a person who knew the data, with the matcher confirming them.
Nothing here shows the matcher can lead. Fixes, in order: a multilingual model, per-catalog
threshold calibration, and demoting the matcher to a hint behind human search.

Until the first two, this is sound infrastructure with a known-poor recommender attached — and
saying so now is cheaper than a city discovering it.
