---
layout: default
title: "Procurement: the framework has the slot and it is empty"
author: Devin Balkind
date: 2026-09-18 14:40:00 -0400
---

Added public procurement as a third category to
[`probe/category_gaps.py`](https://github.com/sarapis/undatacommons-nyc/blob/main/probe/category_gaps.py),
expecting the elections result again — no indicator, lots of city data. The first run said exactly
that: **zero of 519 named indicators**, 150 datasets across 28 cities.

It was wrong, and finding out why produced a better result.

## The method was searching names, and a quarter of the framework has none

`SG_SCP_PROCN` sits in the SDG goal tree. It is the 12.7.1 series — sustainable public procurement
— and it carries **no name**, so a search over indicator *names* cannot see it. Neither can it see
`SG_SCP_PROCN_HS` or `SG_SCP_PROCN_LS`.

We have known since Wednesday that 170 of the 689 base indicators return no name. What we had not
done is account for them when claiming a concept is *absent*. The category search now looks at
DCID mnemonics too, and reports them as **candidates for a human to read** rather than counting
them — mnemonics are noisy, and `SE_ACS_ELECT` is schools with access to *electricity*, not
elections.

## What the slots actually contain

All three procurement DCIDs exist. All three hold **zero observations for zero countries**.

The one adjacent indicator that does carry data is `SG_SCP_CNTRY` — *countries with sustainable
consumption and production national action plans* — and its value is **1** for all 75 countries
that report it. Nobody reports a 0. It is a list of countries that have a plan, recorded as a
number.

So the framework does not lack a procurement indicator. It has three, and they are empty; and the
thing next to them that works counts whether a country has written a policy down.

Against that, **28 cities publish 150 procurement datasets** — tenders, awards, vendors, purchase
orders. New York City alone registers **55,806 contracts worth $147 billion**, every one with an
agency, a vendor, a value and a status.

## The pattern, now three for three

| Category | What the framework measures | What cities publish |
|---|---|---|
| Records access | 16.10.2 — whether a country has *adopted* guarantees | 8 cities: requests filed, answered, how long they took |
| Procurement | 12.7.1 — three empty slots; the neighbour counts action plans | 28 cities: 150 datasets of actual transactions |
| Elections | nothing at all | 23 cities: 469 datasets of results by polling station |

Twice the framework asks **has a policy been adopted** and the cities answer **here is what
happened**. Once it does not ask.

## Procurement is the sturdiest of the three

By this project's own evidence rule — count cities, not datasets — procurement is the best of them:

- **28 cities**, against 23 for elections and 8 for records access.
- **No dominant publisher.** New York is 24% of the procurement datasets. Milan is 66% of the
  election datasets and Chicago 64% of the request logs. Procurement is the one category that is
  not mostly one city's filing habit.

One honest wrinkle: procurement datasets are **not** unusually far from the framework in embedding
space — mean affinity 0.393 against 0.407 for municipal data generally, and only 32% fall in the
bottom quartile of their own catalog, against 64% for elections. The reason is that a procurement
dataset is *about* something — road contracts, health contracts, water contracts — and those
subjects do have indicators. The data gets absorbed by its topic rather than recognised as
procurement. The lexical search is what makes the gap visible; the embedding would have missed it.

## Also true of the other two

Every unnamed DCID the mnemonic search surfaced across all three categories — 19 of them, including
the democratic-institutions and judiciary series `SG_DMK_JDC*` and `SG_DMK_PARLCC_*` — holds
**zero observations**. Unnamed and empty are the same set. That is consistent with Wednesday's
`--all` sweep, where 207 of the 247 indicators outside the usable set returned no country data at
all, and it is worth stating plainly: **the framework's governance slots are largely unfilled, not
merely unnamed.**

Procurement is now a third block on the [demo](https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html),
and `mcp/smoke.py` (32 checks) asserts the empty-slot claim against the artifact, so it cannot
quietly become false if the platform fills them in.
