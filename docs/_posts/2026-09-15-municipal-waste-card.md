---
layout: default
title: "A fifth card, and the caveat runs the other way"
author: Devin
date: 2026-09-15 17:00:00 -0400
---

Added **municipal waste collected** — the indicator the United States does not report to the UN at
all. `EN_MWT_COLLV` has **zero US observations** in every year; ninety other countries report it.

So this is the case where a city can be placed among the world *because* its own country is absent
from the table. There is no US line on the chart, and that is not a gap in our pipeline.

**NYC: 397.9 kg per person (2019), 41st of 91** — between Hungary and Belarus. Its own series runs
from 453.6 kg in 2005 to 387.6 in 2024, about 15% less waste per New Yorker over two decades.

## Why this card earns its place

The caveat does not merely qualify the reading — it **reverses** it, and in the opposite direction
to the recycling card two sections above.

DSNY collects from residences and institutions only; commercial waste goes to private carters and
never appears. The UN definition includes commercial waste. So NYC's figure is an **undercount**,
its true per-capita is higher, and its true rank is **worse** than 41st.

The same residential-only gap makes NYC look *worse* on the recycling chart and *better* here —
because it sits in the numerator there and is simply missing here. **One definitional difference,
two opposite distortions, on one page.** That is a stronger demonstration than either chart alone,
and it is not a point we could have made before the world view existed.

## An assumption stated rather than buried

DSNY publishes **"Tons"** and never says short or metric. US municipal practice is short tons, so
that is what we assumed (×0.90718) — and the card says so, along with the consequence: if the
figures are metric, every NYC number here is about 10% low.

An undocumented unit is not a reason to skip the comparison. It is a reason to put the assumption
on the face of the chart where a reader can disagree with it.

## What we did not add

Three other domains looked promising and were checked before anything was built:

- **Suicide mortality** — the NYC dataset carries two different ICD code strings across years, has
  no "All Sexes" aggregate, and switches the sex encoding (`F` / `Female`) mid-series.
- **Broadband** — a single snapshot with no year field, measuring *household* adoption share
  against the UN's *subscriptions per 100 inhabitants*.
- **Electronic waste** — thin coverage, and a second waste chart making the same point.

Three for three, the NYC side was the binding constraint. That has been the pattern since the
first day of this project, and it is the opposite of what we expected going in.
