---
layout: default
title: "The whole corpus: what the other 247 indicators hold"
author: Devin Balkind
date: 2026-09-16 18:15:00 -0400
---

The [smell test](https://sarapis.github.io/undatacommons-nyc/artifacts/smell-latest) ran against
the **442 indicators screened usable**. That left 247 graded `NO-DATA` or `THIN-COVERAGE` — and
the grade was assigned against a **six-country panel**, so it only ever meant "no data for those
six", not "no data anywhere". Ran it with `--all` to find out.

**689 indicators · 773,335 observations · 2,503 findings.**

## The screening panel was right, and now that is measured

The extra 247 indicators contributed **5,056 observations — 0.65% of the corpus** — and **207 of
the 247 returned no country-level data at all.** A grade assigned on six countries predicted
global emptiness correctly 84% of the time.

That closes a question I had raised against our own method. The six-country panel was chosen for
speed, with the honest caveat that it could not distinguish "the panel does not report this" from
"nobody does". It turns out to distinguish them almost perfectly, and **442 remains the right
denominator** for everything downstream.

The 40 indicators that *do* hold data are worth knowing about, because of what they are: e-waste
collected, recycled and its proportions; municipal waste imported and exported. Those sit exactly
in the band we identified months ago as the interesting one — **indicators a city can report
internationally precisely because its own country skips them.**

## Guadeloupe, again, four times over

The previous sweep found Guadeloupe's e-waste collection multiplying by a thousand in 2022. With
the full corpus it turns out the same error propagates through **every derived indicator**:

| Indicator | Unit | 2021 | 2022 |
|---|---|---:|---:|
| Electronic waste collected per capita | kg | 13.71 | **13,950** |
| Electronic waste recycled per capita | kg | 13.71 | **13,950** |
| Total electronic waste collected | tonnes | 5,472 | **5,367,000** |
| Total electronic waste recycled | tonnes | 5,472 | **5,367,000** |

The largest total any other country has ever recorded for e-waste recycled is 899,300 tonnes. So
**Guadeloupe — population about 380,000 — is published as the world's biggest e-waste recycler,
by a factor of six.** One unit slip in a 2022 submission, carried into four indicators.

This is also the first time the checks corroborated each other: the same anomaly surfacing in
four related series is much stronger evidence than the same anomaly surfacing once.

## Small states reporting zero for two decades

The new coverage brought a pattern rather than a single error. Municipal waste **exported** and
**imported**, both flatlined at exactly zero for very long runs: Mauritius 23 years, Dominica 22,
Singapore 21 and 22, Cuba 20, Palestinian Territories 19, Jamaica 18, Saint Lucia 16,
Liechtenstein 24.

Some of that is surely true — a small island genuinely exports no municipal waste. But a
twenty-year run of exact zeros is also what "no submission" looks like when it is stored as a
number instead of a gap, and the two are indistinguishable from outside. Worth one question to
the platform team: **is zero here a measurement or a default?** Our own rule is that a missing
year stays missing and is never interpolated; the same distinction matters just as much in the
other direction.

Alongside it, "Proportion of electronic waste that is collected" sits at exactly **100%** for
Niger for eight consecutive years and Iran for six.

## Everything else held

The finding counts barely moved — 2,457 to 2,503, with one new HIGH — which is the correct result
for adding 0.65% more data. The five verified errors from the earlier sweep stand unchanged.
