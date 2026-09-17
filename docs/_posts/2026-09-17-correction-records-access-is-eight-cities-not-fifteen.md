---
layout: default
title: "Correction: records access is eight cities, not fifteen"
author: Devin Balkind
date: 2026-09-17 15:05:00 -0400
---

Wiring the inverse crosswalk's two headline categories into the demo meant checking their numbers
a second way, and one of them did not survive.

**[The 16 Sep write-up](https://sarapis.github.io/undatacommons-nyc/activity) said fifteen cities
publish records-access request logs. Counted properly it is eight.**

The fifteen was **cluster membership** — how many cities contributed a dataset to the k-means
cluster whose distinctive terms were *foia, request, log*. That is not the same as how many cities
publish a request log. The cluster had swept in Edmonton's *Media Releases* and NYC's *City Hall
Library Catalog*, which sit near request logs in embedding space and are not request logs.

`probe/category_gaps.py` now counts the same categories without any clustering: search every named
SDG indicator for the category's vocabulary, and count the municipal datasets whose **titles**
carry it, in six languages. Both halves are greppable.

| | Cluster membership | Vocabulary count |
|---|---:|---:|
| Records-access requests | 15 cities | **8 cities · 73 datasets** |
| Electoral administration | 10 + 6 cities, two runs | **23 cities · 469 datasets** |

Elections went *up*, which is the useful part of the check: clustering was splitting one category
across two runs and under-counting it, while over-counting the other. A method that is wrong in
both directions is not a method you can read a number off.

## What this does not change

The argument for both gaps stands, and the elections one is stronger than before:

- **Zero of the 519 named indicators** mention an election, a vote or a turnout.
- **One** mentions access to information — SDG 16.10.2, which asks whether a country has *adopted*
  guarantees. The framework measures whether a law exists; the cities measure whether it works.
- For **35** of the 469 election datasets, the closest concept in the entire framework is
  *municipal waste collected*.

## The rule this leaves behind

**A cluster is not a count.** k-means returns *k* groups whether or not *k* categories exist, and
its membership is the nearest thing to a centroid, not the things that belong to a category. We had
already made it declare its own coherence and publish 14 of 40 clusters as diffuse. This goes
further: where a category can be counted lexically, the lexical count is the one that gets
published, and the cluster is what *found* it rather than what measures it.

Both categories are now on the [demo](https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html),
with the smaller, checkable numbers — and `mcp/smoke.py` asserts the page against
`probe/category_gaps.py`, so they cannot drift apart.
