---
layout: default
title: "Fixed: the matcher now finds Vision Zero Fatality Records — and NYC got better too"
author: Devin
date: 2026-09-16 15:00:00 -0400
---

Boston's *Vision Zero Fatality Records* ranked **23rd of 235** for "death rate due to road traffic
injuries", below a contract-award file. It now ranks **1st**. NYC's ground-truth median improved
from 23 to 14 at the same time.

## The diagnosis was not the query

First instinct was query expansion — add "crashes, collisions, fatalities, vision zero" to the
indicator name. It made things **worse** (rank 23 → 30). So did rephrasing: "traffic fatalities"
scored *worse* (32) than the clinical UN wording (23).

The problem was the document, not the query. Vision Zero Fatality Records carries **excellent**
metadata:

```
title: Vision Zero Fatality Records
tags:  accidents bikes cars crashes fatalities pedestrians safety streets traffic vision zero
desc:  1,500 characters of programme mission statement — "our commitment to focus
       the city's resources on proven strategies… we are inspired by…"
```

A static embedding averages over every token. Sixty characters of exactly-right title and tags
were being drowned by 1,500 characters of boilerplate. The dataset that beat it, *My Neighborhood
Dataset*, won partly by having a **shorter** description.

## The fix: score each field separately, take the best

Two vectors per dataset instead of one concatenated blob:

- **head** — title, category, tags, column names: the structured, high-signal fields
- **body** — description truncated to 600 characters, plus column descriptions

Score is `max(head·q, body·q)`, so a dataset surfaces on whichever field actually carries its
signal. Programme-named datasets are found by their tags; thinly-titled ones by their prose.

Measured both ways before adopting it:

| Scheme | NYC median rank | top-10 | top-50 | Boston: Vision Zero |
|---|---:|---:|---:|---:|
| concatenated (before) | 23 | 3/7 | 5/7 | #23 |
| head only | 57 | 3/7 | 3/7 | #1 |
| **max(head, body)** | **14** | 3/7 | 5/7 | **#1** |

Head-only fixes Boston and wrecks NYC — PM2.5 falls from rank 30 to 397, because NYC's air-quality
dataset is found through its description. Taking the max gets both.

Boston now returns *Vision Zero Fatality Records* (0.544) and *Vision Zero Crash Records* (0.541)
as the top two for road deaths.

## A silent cache bug found on the way

Vector caches were keyed by city and model but **not by the text representation**. Changing how
documents are built silently reused vectors from the old scheme — wrong rankings, no symptom, no
error. Some of the earlier Boston numbers were affected by exactly this.

The cache key now includes a `REPR_VERSION` that must be bumped when the representation changes.
Fourth entry in this project's running list of automated checks that were confidently wrong.

## Still not solved

This improves retrieval; it does not make the matcher trustworthy. The cities now surface their
obvious datasets, and a person still has to decide whether *Vision Zero Fatality Records* is
comparable to SDG 3.6.1 — which, per the spec, is the one thing a machine may not do.
