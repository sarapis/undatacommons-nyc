---
layout: default
title: "A smell test for the UN graph, and five things it found"
author: Devin Balkind
date: 2026-09-16 16:40:00 -0400
---

Malaysia reports recycling 147.7% of its municipal waste. That figure is in authoritative UN
data, it is on our demo, and we found it by accident while building a chart. This is the obvious
follow-up, run properly: **442 indicators, 768,279 observations, every reporting country and
every year**, against checks dumb enough that they need no subject-matter knowledge — a
percentage above 100, a negative count, a rate exceeding its own denominator, a value repeated
across countries that should not agree.

[Full results](https://sarapis.github.io/undatacommons-nyc/artifacts/smell-latest) ·
`python3 probe/smell.py`

**The tool flags; it does not judge.** Everything below that I call an error, I checked by hand
against the indicator's own distribution first.

## Five that are wrong

**1. Kyrgyzstan feels 6,990% safe walking home.** SDG 16.1.4, *proportion of population that feel
safe walking alone around their local area after dark*, unit `Percent`:

| Kyrgyzstan | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|
| | 57.9 | 64.35 | 66.8 | **6710** | **6840** | **6990** |

The other 252 observations, across 55 countries, run from 22.8 to 95.0, median 72.0. Divide the
last three by 100 and you get 67.1, 68.4, 69.9 — which continues Kyrgyzstan's own trend from 66.8
exactly. Live for three consecutive years.

**2. South Africa recycles 1.86 billion tonnes of municipal waste.** Global municipal solid waste
generation is roughly 2 billion tonnes a year, worldwide. South Africa's own earlier figures are
260,600 t (2005) and 520,800 t (2006); from 2018 they are 1.0–3.4 **billion**. Read as kilograms
they are entirely sensible.

**3. Brunei generates 12,580 tonnes of hazardous waste per person.** `EN_HAZ_PCAP`, unit
kilograms, where the global median is 22 kg and the maximum outside Brunei is 212. Brunei reports
8.7–36 million kg **per capita**, every year from 2016 to 2023. Against a population of ~450,000
that is 5.7 billion tonnes. It looks like a national total sitting in a per-capita field.

**4. Guadeloupe's e-waste collection multiplies by a thousand in one year.** 8.46, 8.54, 10.03,
10.36, 10.58, 11.97, 13.10, 13.71 — then **13,950** in 2022. The cleanest of the five: the series
resumes perfectly if you divide the last point by 1,000.

**5. Malawi is paid to send remittances.** `SI_RMT_COST`, the average cost of sending $200, as a
percentage. Malawi runs 16.95, 15.82, 14.47, 16.26, 14.79, 13.13 — then **−0.1** and **−0.93** —
then 31.48. A cost of minus one percent, for two years, between normal values.

## One that is not an error, and matters more

**The United States recorded 345,600 disaster deaths in 2020 and 470,600 in 2021.** Every other
country in `VC_DSR_MORT` has a median of 42. Those are COVID-19 deaths: the US classified the
pandemic as a disaster and reported it here. Most countries did not.

That is not a data error. It is the exact failure this whole project exists to prevent — two
numbers that share a variable, a unit and an axis, and are not the same measurement. A chart of
"disaster deaths, US vs peers" would be perfectly well-formed and would tell you something false.
It is the strongest argument yet for the comparability grade, and we found it with a check that
knows nothing about disasters.

## Four that look wrong and are not

Each of these I chased and dropped, which is most of what the afternoon consisted of:

- **Kuwait's water stress, 3,850%.** Correct. Withdrawal beyond renewable resources via
  desalination and fossil groundwater. 371 observations exceed 100% across 17 countries.
- **Marshall Islands, 132,810 disaster-affected persons per 100,000.** Correct. A person counts
  once per disaster, so a small state hit repeatedly exceeds its own population. My check's
  premise — "more events than there are people to have them" — was simply wrong.
- **Euro-area countries sharing a conversion factor of 1.08271; Benin, Burkina Faso and Cameroon
  sharing 710.208.** Correct. The check found the euro and the CFA franc.
- **23,172 negative percentages.** Correct, nearly all of them. "Annual growth rate of real GDP
  per capita", "Current account balance as a proportion of GDP", "Change in minimum river flow
  (%)" — the graph's `Percent` unit covers **both bounded proportions and signed rates**, and no
  unit string distinguishes them.

## What the checks learned about themselves

The first full sweep returned **41,350 findings** — 5.4% of all observations, which is not a
result, it is a broken instrument. Three false-positive classes, each caught by reading rows
rather than totals:

| Check said | Actually |
|---|---|
| 351 jumps in one indicator (12% of its rows) | the Indicator of Food Price Anomalies is a **signed index centred on zero**; a ratio means nothing on it |
| 23,172 negative percentages | growth rates and balances are signed by construction |
| four scaled rates treated as plain counts | my substring match on `"COUNT"` swallowed `RATIO_COUNT_PER_100_COUNT_POP`, so its cap never applied |

The first fix over-corrected: it gated the jump check on a unit whitelist, and thereby discarded
Mauritius' food waste going **207 tonnes → 177,570 tonnes in a year** because `WEIGHT_TN` was not
on the list. Gating on the *shape* of the quantity — does this indicator ever go negative
anywhere? — keeps it.

What came out of that is a principle worth more than any individual finding: **an indicator is its
own control group.** A rule broken by most of an indicator's observations is its definition. A
rule broken by three country-years out of three thousand is Kyrgyzstan. So checks are now
suppressed per-indicator when they fire often enough to be structural — **165 suppressed groups,
38,943 would-be findings** — and the suppressions are published, because the list of indicators
that publish signed values under a `Percent` unit is itself a finding about the graph's
vocabulary.

That left an `outlier` check that works against each indicator's own distribution rather than
against what a unit is supposed to mean: 20× the indicator's 99th percentile. It survives
suppression, which matters — "proportion of hazardous waste treated" exceeds 100% for 37
countries, so its range check is structural and gets dropped, and Guatemala's **44,825%** would
have gone with it. It is also the only check that reaches the **123 indicators and 248,457
observations** whose units (`CR_USD`, `WEIGHT_TN`, `INDEX`, `SCORE`) have no meaningful range at
all. The report states that coverage gap on its own face.

Final count: **2,457 findings, 92 of them HIGH.** Small enough to read.

## What this is for

Two things. It is a QA gate on the data our own crosswalk depends on — and it is the kind of
thing only an outsider runs, because it requires no authority and no access, just the published
graph and a willingness to look at 768,279 numbers. The five errors above are reportable to the
platform team as they stand.
