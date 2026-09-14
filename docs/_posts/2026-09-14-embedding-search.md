---
layout: default
title: "Embedding search: correct dataset moves from median rank 1535 to 23"
author: Devin
date: 2026-09-14 14:00:00 -0400
---

Replaced the keyword matcher. The headline is not that embeddings are better — it is *how
much*, and that we measured it instead of assuming.

## The measurement

Ground truth is the seven NYC datasets already verified by hand in `crosswalk.json`. The
question: out of 2,400 datasets, where does each method rank the correct one?

| Method | Median rank | top-10 | top-50 |
|---|---:|---:|---:|
| Keyword overlap | **1535** | 2/7 | 2/7 |
| Embeddings (name + description) | 27 | 2/7 | 4/7 |
| Embeddings (+ columns, tags, category) | **23** | 3/7 | 5/7 |

A ~65× improvement in median rank. Keyword overlap was not merely imperfect — at a median rank
of 1535 out of 2400 it was **worse than useless**, since it ranked the right answer below the
midpoint of a random shuffle. Every "candidate" it produced was effectively arbitrary.

## Two changes, and the second was the surprise

**Retrieval over the whole catalog.** The old matcher could only re-rank whatever Socrata's
keyword search returned, so retrieval was the real ceiling, not scoring. All 2,400 datasets are
now cached and embedded locally.

**Columns, tags and category are worth as much as the description.** Adding them moved
*Proportion of municipal waste recycled* → DSNY Monthly Tonnage from rank **882 to 23**, because
the dataset's title never says "recycled" — the concept lives in its fields and its tags.

## What it still cannot do, and why that is structural

Two of the seven stay unfindable at any rank. NYC's homicide series is **offence code 101 inside
"NYPD Complaint Data Historic"** — a fact that appears nowhere in that dataset's metadata. No
text method can recover a mapping that depends on knowing what is *inside* a dataset.

So roughly 30% of real mappings need human domain knowledge and always will. That is the
argument for the shortlist being a triage aid with a person in the loop, which is the same
conclusion as the grade veto and for the same reason.

## Result

248 GREEN → 73 excluded as inherently national → **53 with a candidate above the similarity
floor, 50 not yet in the crosswalk.** Eyeballing the top of the list, most are now plausible
rather than most being noise.

New finds the keyword matcher never surfaced:

- **Fixed broadband subscriptions** → Broadband Adoption and Infrastructure by Community District
- **CO2 emissions from fuel combustion** → Office of Climate and Sustainability GHG inventory
- **Government consumption expenditure growth** → Mayor's Management Report Spending and Budget

## Dependency

`pip3 install model2vec` — static embeddings, CPU-only, no torch, tens of megabytes. Without it
the pipeline falls back to keyword matching and prints exactly how bad that is. The repo keeps
its clone-and-run property; it is just measurably worse in that mode.

The similarity floor of 0.50 is a calibration choice with no theory behind it — the median top
candidate across all indicators is 0.46, so it keeps roughly the better half.
