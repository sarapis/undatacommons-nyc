---
layout: default
title: Data quality report — updated 2026-09-18
---

# UN System Data Commons — seven data quality issues, with evidence

**For the UN System Data Commons platform team.** Prepared 16 Sep 2026, **widened 18 Sep** from the
SDG goal framework to the whole governed graph — which more than doubled the surface and added two
errors. By the NYC Voluntary Local Review team (Builders' Day participants), offered constructively — we are building a city↔UN
indicator crosswalk and these surfaced while checking the data our own work depends on.

**How they were found.** A sweep of the governed corpus — **1,661 indicators, 1,701,211
observations, every reporting country and every year** — against plausibility checks that need no
subject-matter knowledge: a percentage outside 0–100, a negative count, a rate exceeding its own
denominator, a value far outside its own indicator's distribution. One
`get_child_observations(variable, Earth, Country, date="all")` call per indicator.

Source: [`probe/smell.py`](https://github.com/sarapis/undatacommons-nyc/blob/main/probe/smell.py) ·
full output: [smell test artifact](https://sarapis.github.io/undatacommons-nyc/artifacts/smell-latest)

**Every item below was checked by hand** against the indicator's own distribution before being
included. The sweep produced 3,844 findings; these are the seven we are confident are errors, plus
one that is not an error and matters more. Issues we investigated and **dismissed** are listed at
the end, so you can see what the checks get wrong.

---

## Summary

| # | Indicator | Country | Problem | Confidence |
|---|---|---|---|---|
| 1 | `VC_SNS_WALN_DRK` — feel safe walking alone after dark | Kyrgyzstan | ×100 scale error, 2021–23 | High |
| 2 | `EN_MWT_RCYV` — municipal waste recycled | South Africa | ×1,000 (kg reported as tonnes), 2018–23 | High |
| 3 | `EN_HAZ_PCAP` — hazardous waste per capita | Brunei | National total in a per-capita field, 2016–23 | High |
| 4 | `EN_EWT_*` — e-waste, **four** indicators | Guadeloupe | ×1,000, 2022, propagated across all four | High |
| 5 | `SI_RMT_COST` — average remittance cost | Malawi, Myanmar | Negative cost | High |
| 6 | `STR_WORK_NB` — workers in strikes and lockouts | Brazil | 1.28 **billion** workers, 2015 | High |
| 7 | `EAR_INEE_NB_PPP` — minimum wage in PPP int'l dollars | Slovenia | Unconverted tolar, 2000–06 | High |
| — | `VC_DSR_MORT` — deaths due to disaster | United States | Not an error; a comparability hazard | — |

---

## 1. Kyrgyzstan: safety percentage is 100× too large

**`undata/sdg/VC_SNS_WALN_DRK`** — *Proportion of population that feel safe walking alone around
the area they live after dark*. Unit `Percent`. Provenance `unstats.un.org/sdgs/dataportal`,
sourceId `3722936608695937273`.

| Year | 2018 | 2019 | 2020 | **2021** | **2022** | **2023** |
|---|---:|---:|---:|---:|---:|---:|
| Kyrgyzstan | 57.9 | 64.35 | 66.8 | **6710** | **6840** | **6990** |

The indicator holds 258 observations across 56 countries. **Every other observation falls between
22.8 and 95.0**, median 72.0.

**Mechanism:** dividing the three values by 100 gives 67.1, 68.4, 69.9 — which continues
Kyrgyzstan's own trend from 66.8 (2020) smoothly. Consistent with a submission in basis points, or
a proportion multiplied by 10,000 rather than 100.

**Suggested correction:** 67.10, 68.40, 69.90.

---

## 2. South Africa: municipal waste recycled exceeds world output

**`undata/sdg/EN_MWT_RCYV`** — *Municipal waste recycled*. Unit `WEIGHT_TN` (tonnes). sourceId
`11758492570122983502`.

| Year | 2005 | 2006 | **2018** | **2019** | **2020** | **2021** | **2022** | **2023** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| South Africa (t) | 260,566 | 520,844 | **1.86×10⁹** | **3.44×10⁹** | **1.02×10⁹** | **2.22×10⁹** | **1.46×10⁹** | **1.33×10⁹** |

Global municipal solid waste *generation* is on the order of 2×10⁹ tonnes per year. The 2019 value
alone would be more than 1.5× all municipal waste generated on Earth. Across the other 114
countries the maximum ever recorded is **6.27×10⁷ tonnes**, and the median is 444,000.

**Mechanism:** the values read as kilograms. 1.86×10⁹ kg = 1,855 kt, which against South Africa's
own 2006 figure of 521 kt is plausible growth over twelve years.

**Suggested check:** whether the 2018– series changed submission units from the 2005–06 series.

---

## 3. Brunei: national total placed in a per-capita field

**`undata/sdg/EN_HAZ_PCAP`** — *Hazardous waste generated, per capita*. Unit `WEIGHT_KG`. sourceId
`6461446536147282263`.

Brunei, every year 2016–2023: **8.68×10⁶ to 3.61×10⁷ kg per person.** Across the other 116
countries the median is **22.0 kg** and the maximum is 211,720.

At 3.61×10⁷ kg per capita and a population near 450,000, the implied national total is 16 billion
tonnes of hazardous waste per year.

**Mechanism — this one identifies itself.** Divide the reported value by Brunei's population:

`1.2575×10⁷ kg ÷ ~450,000 people ≈ 28 kg per capita`

against a global median of 22.0. The national total, in kilograms, has been written into the
per-capita field. Every year from 2016 to 2023 behaves the same way.

---

## 4. Guadeloupe: one 2022 unit slip, propagated through four indicators

All four share sourceIds `6461446536147282263` (per-capita) and `11758492570122983502` (totals).

| Indicator | Unit | 2020 | 2021 | **2022** |
|---|---|---:|---:|---:|
| `EN_EWT_COLLPCAP` e-waste collected per capita | kg | 13.10 | 13.71 | **13,951.2** |
| `EN_EWT_RCYPCAP` e-waste recycled per capita | kg | 13.10 | 13.71 | **13,951.2** |
| `EN_EWT_COLLV` total e-waste collected | t | 5,337 | 5,472 | **5,367,000** |
| `EN_EWT_RCYV` total e-waste recycled | t | 5,337 | 5,472 | **5,367,000** |

Guadeloupe's per-capita series is otherwise smooth and unremarkable across fourteen years: 1.91,
3.94, 6.33, 7.20, 7.23, 7.32, 8.46, 8.54, 10.03, 10.36, 10.58, 11.97, 13.10, 13.71.

**The consequence is visible at world level.** The largest total e-waste recycled ever recorded by
any other country is **899,287 tonnes**. Guadeloupe's 2022 figure of 5,367,000 tonnes makes a
territory of roughly 380,000 people the world's largest e-waste recycler **by a factor of six**.

**Mechanism:** a ×1,000 unit slip in the 2022 submission (≈1017× on the per-capita figures, ≈981×
on the totals), carried into every derived indicator.

**Suggested correction:** 13.95 kg per capita; 5,367 tonnes.

---

## 5. Negative remittance costs

**`undata/sdg/SI_RMT_COST`** — *Average cost of sending $200 to a receiving country, as a
proportion of the amount remitted*. Unit `Percent`.

| Malawi | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | **2023** | **2024** | 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| | 16.95 | 15.82 | 14.47 | 16.26 | 14.79 | 13.13 | **−0.10** | **−0.93** | 31.48 |

Myanmar 2022 carries **−0.56** on the same indicator, and Ghana 2022 carries **−4.04** on the
corresponding *sending-country* indicator.

A cost expressed as a proportion of the amount remitted cannot be negative, and in Malawi's case
the two negative years sit between 13.13 and 31.48.

---

## 6. Brazil: 1.28 billion workers involved in strikes

**`undata/ilo/STR_WORK_NB`** — *Number of workers involved in strikes and lockouts*. Unit
`COUNT_PERSONS`. 1,178 observations across 91 countries.

| Brazil | 2010 | 2011 | 2012 | **2015** | 2016 | 2017 |
|---|---:|---:|---:|---:|---:|---:|
| workers | 1,582,750 | 2,050,020 | 1,771,950 | **1,284,680,000** | 761,000,000 | 364,600,000 |

Brazil's population is about 210 million. The 2015 figure is **six times the entire population**,
and **fourteen times the 92,324,000 maximum any country has ever recorded** on this indicator. The
global median is 9,831.

Brazil's own series runs between 0.8 and 3.8 million from 2000 to 2012, so 2015 is a break of
roughly **400×** against its own history, and 2016–2019 stay in the hundreds of millions before
returning to normal.

**Suggested check:** whether the 2015– figures are worker-*days* or some cumulative measure rather
than a count of persons.

---

## 7. Slovenia: unconverted tolar in an international-dollar field

**`undata/ilo/EAR_INEE_NB_PPP`** — *Monthly minimum wage in international dollars at Purchasing
Power Parity rates*. Unit `CR_USD_PPP_2021`. 3,369 observations across 162 countries.

| Slovenia | 2000 | 2002 | 2004 | 2006 | **2007** | 2008 | 2010 |
|---|---:|---:|---:|---:|---:|---:|---:|
| | 159,122 | 170,774 | 109,986 | 116,837 | **763** | 826 | 1,050 |

The global median is **382** and the maximum any country has ever recorded is **10,259**. Slovenia's
2000–2006 values are ten to seventeen times that maximum.

**The break is diagnostic.** It falls exactly at **2007 — the year Slovenia adopted the euro** — and
every value from 2007 onward is unremarkable. The pre-2007 figures read as Slovenian tolar that
were never converted into the PPP international dollars the unit declares. At roughly 240 tolar to
the euro, 170,774 tolar is about 712 euro, which is the right order for the 2007 figure of 763.

**Suggested check:** whether other pre-euro-accession members carry the same pattern in this series.

---

## Not an error, and more important than any of the above

**`undata/sdg/VC_DSR_MORT`** — *Number of deaths due to disaster*. Unit `COUNT`.

| United States | 2015 | 2016 | 2017 | 2018 | 2019 | **2020** | **2021** |
|---|---:|---:|---:|---:|---:|---:|---:|
| | 698 | 668 | 3,847 | 772 | 570 | **345,950** | **470,644** |

Across the other 163 countries the median is **42** and the all-time maximum is 222,608. The US
2020 and 2021 values track reported national COVID-19 mortality closely. The United States appears
to have classified the pandemic as a disaster and reported it here; most countries did not.

**This is presumably correct reporting, and that is the problem.** Two numbers share a variable, a
unit and an axis, and are not the same measurement. A chart of "disaster deaths, US vs peers"
would be perfectly well-formed and would mislead every reader. There is nothing in the observation
metadata — unit, observation period, provenance — that would let a tool detect it.

For a platform whose value rests on cross-national comparison, we think this is worth a
machine-readable signal at the observation level: a note, a flag, or a method qualifier that a
client can surface on the face of a chart. We would be glad to discuss it at Builders' Day; it is
the single clearest case we have found for the comparability grading our project is built around.

---

## Two open questions, not claims

**Is zero a measurement or a missing submission?** `undata/sdg/EN_MWT_EXP` and
`undata/sdg/EN_MWT_IMP` (municipal waste exported/imported) carry exact zeros for very long unbroken runs: Liechtenstein 24 years,
Mauritius 23, Dominica 22, Singapore 21 and 22, Cuba 20, Palestinian Territories 19, Jamaica 18.
Some of this is certainly true of small islands. But a two-decade run of exact zeros is also what a
non-submission looks like when stored as a number rather than a gap, and from outside the two are
indistinguishable.

**Twelve years of a flat negative.** `undata/unaids/INF_AVRT` — *new HIV infections averted by
prevention of mother-to-child transmission*, unit `COUNT_INFECTIONS`. Mozambique reports **−15.6
for twelve consecutive years, 1990–2001**, varying only in the third decimal, then +18.6 in 2002 and
+187 in 2003. We understand this is modelled as a counterfactual difference, so a negative is not
in itself impossible — but a *flat* negative across twelve years before the programme existed looks
more like a baseline offset than a measurement. The global median is 11.7.

**100% collection rates.** `undata/sdg/EN_EWT_COLLR` (*proportion of electronic waste that is
collected*) sits at exactly 100 for Niger for eight consecutive years (2012–2019) and Iran for six
(2018–2023).

---

## What we checked and dismissed

Included so you can judge the checks' precision rather than take it on trust. Each of these looked
like a finding and is not:

- **Kuwait's water stress at 3,850%** (`ER_H2O_STRESS`). Correct — withdrawal beyond renewable
  resources via desalination and fossil groundwater. 371 observations exceed 100% across 17
  countries.
- **132,810 disaster-affected persons per 100,000 in the Marshall Islands** (`VC_DSR_DAFF`).
  Correct — a person counts once per disaster, so a state hit repeatedly in one year exceeds its
  own population. Our check's premise was wrong, not the data.
- **Euro-area countries sharing a conversion factor of 1.08271; Benin, Burkina Faso and Cameroon
  sharing 710.208.** Correct — the check had found the euro and the CFA franc.
- **Iran's monthly minimum wage, 23× the indicator's 99th percentile.** Correct. The unit is
  `CR_LCU` — **local currency** — so 53 million is an ordinary monthly wage in rial and absurd in
  euro. Our outlier check compares every country's values within an indicator, which is meaningless
  on a local-currency series; it now skips them. Worth noting as a general hazard for anyone
  building automated checks on this graph.
- **23,172 negative percentages.** Correct, nearly all. "Annual growth rate of real GDP per
  capita", "Current account balance as a proportion of GDP", "Change in minimum river flow (%)".
  Which leads to the one structural observation we would offer:

> **The `Percent` unit covers both bounded proportions and signed rates of change**, with nothing
> in the unit string to tell them apart. Any automated quality check — ours or yours — has to
> infer the difference from the data rather than read it from the metadata. A distinct unit, or a
> `bounded: [0,100]` property, would make a large class of errors mechanically detectable. Our
> workaround is to treat each indicator as its own control group: a rule broken by most of an
> indicator's observations is its definition, and one broken by three country-years in three
> thousand is an error.

---

## A third structural item

Alongside the 170 unnamed indicators and the `Percent` unit, one more that surfaced from widening
the sweep: **enumerating the corpus depends on where you start, and no entry point sees everything.**

Walking `->relevantVariable` from `undata/topic/Root` yields **1,661 base indicators**; walking from
the seventeen SDG goal trees yields **689**. That much is expected — the goal framework is a subset.
What is not expected is that **six indicators are reachable from the goal trees and not from Root**:

```
undata/sdg/SG_DSR_SILN   undata/sdg/SG_DSR_SILS   undata/sdg/SM_POP_REFG_OR
undata/sdg/VC_DSR_AGLH   undata/sdg/VC_DSR_CHLN   undata/sdg/VC_DSR_HOLH
```

All seventeen goal trees are direct children of Root — 17 of its 42 — so a traversal from Root
should be a strict superset. Three checks rule out the obvious explanations: neither walk logged a
fetch error, the goal-tree walk is exactly reproducible (re-run two days apart, identical 689), and
the disagreement runs both ways — twelve `undata/sdg/` indicators are reachable from Root and not
from the goal trees, including `SG_DMK_PARLYTH*` and `SE_SGE_*`.

So `->relevantVariable` is not transitive across these hierarchies, and a client enumerating the
corpus from a single root gets a silently incomplete set with no way to detect it. We would want to
know which entry point, if any, is intended to be complete.

## Reproducing

```bash
git clone https://github.com/sarapis/undatacommons-nyc
python3 probe/corpus.py --roots all       # the whole graph, 1,661 indicators
python3 probe/smell.py --all --corpus probe/cache/corpus-all.json
```

Stdlib only. Writes `docs/artifacts/smell-<date>.{json,md}`; the JSON carries every finding with
its DCID, place, year, value, unit and provenance. Any single item above can be checked directly:

```bash
python3 -c "
import sys; sys.path.insert(0,'probe')
from undc import Client
r = Client().call_tool('get_child_observations', {
    'variable_dcid': 'undata/sdg/VC_SNS_WALN_DRK',
    'parent_place_dcid': 'Earth', 'child_place_type': 'Country', 'date': 'all'})
print([x for x in r['data']['rows'] if x[0] == 'country/KGZ'])"
```

Contact: the repo is public at <https://github.com/sarapis/undatacommons-nyc>; we will be at
Builders' Day on 22 September.
