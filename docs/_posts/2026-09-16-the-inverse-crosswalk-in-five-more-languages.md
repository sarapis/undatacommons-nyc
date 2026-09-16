---
layout: default
title: "The inverse crosswalk in five more languages"
author: Devin Balkind
date: 2026-09-16 23:30:00 -0400
---

Ran the [inverse crosswalk](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-latest) over the
non-English catalogs: **5,956 datasets from 11 cities** in Italian, Portuguese, Spanish, German and
Croatian, pooled into one run under the multilingual model.
[Results](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-non-en-latest) ·
`python3 probe/inverse.py --language non-en`

Pooled rather than run per language, because cosine similarities from two different models are not
comparable and two-to-four cities per language could not support an analysis whose unit of evidence
is *how many cities*. Pooled, they share one space and eleven cities.

## Elections, in both language groups, independently

The tightest cluster in anything this project has produced: **241 datasets across 6 cities,
coherence 0.90** — Milan's *Elezioni Politiche: Risultati di Sezione*, Madrid's *Elecciones
Autonómicas*, polling-station-level results going back to 1996.

And the English run found the same thing separately: **election results by voting station, 10
cities, coherence 0.71** — Calgary, Edmonton, and others.

Two disjoint sets of cities, two different embedding models, one category. The SDG framework has no
indicator for electoral administration at all; the nearest thing the matcher can find for the
English cluster is *"number of local governments"*. Turnout, results, polling-station coverage —
cities publish all of it and the framework has no word for any of it.

**COVID-19 case reporting corroborates the same way**: 6 English cities and 7 non-English cities,
independently. The nearest indicators the matcher offers are *"new HIV infections per 1,000
uninfected population"* and *"number of total conflict-related deaths"*. There is no city-level
pandemic-surveillance indicator to match.

## What only the non-English catalogs show

| Cities | Datasets | Theme |
|---:|---:|---|
| 5 | 113 | **Property market valuations** — Italy's OMI *quotazioni immobiliari*, sale and rental prices by zone, half-year by half-year since 2004 |
| 6 | 69 | **Weights-and-measures inspection** — Brazil's Ipem verifications of pre-measured goods |
| 5 | 33 | **Public-employee working arrangements** — Milan's *personale a tempo indeterminato in telelavoro*, permanent staff on telework, by year |

The property-valuation series is the interesting one. Housing affordability is squarely an SDG 11
concern (11.1.1 is inadequate housing), but the framework counts *people in inadequate housing* and
the Italian cities publish *what property costs, by neighbourhood, twice a year, for twenty years*.
Those are not the same measurement and only one of them has an indicator.

## The controls came out better than the English run

**11 of 11 passed**, against 8 of 9 in English. These are hand-built: no city outside NYC has a
graded worksheet, so the controls are datasets whose titles plainly correspond to an SDG concept,
chosen across all five languages and recorded in `probe/inverse_controls.json`.

The two weakest are both Portuguese — Fortaleza's *Número de Óbitos por Acidentes de Trânsito* at
the 44th percentile and Recife's *Acidentes de Trânsito com Vítimas* at the 32nd. Those are about
as unambiguous as a match gets (deaths from traffic accidents ↔ SDG 3.6.1) and they sit in the
bottom half. **Portuguese retrieval is the weakest link, so the Brazilian portion of the tail is
the least trustworthy part of this run**, and anything resting on Fortaleza, Recife, Belo Horizonte
or São Paulo alone should be read with that in mind.

## A quarter of the framework was unmatched text

Both runs improved when I stopped matching against indicators that have no name.

**170 of the 689 base indicators carry no name in any source we hold** — they return neither
metadata nor observations. The first version fell back to the DCID mnemonic, so a quarter of "the
framework" was represented by query strings like `DI ILL OUT`. Nothing can match that, which
inflates the tail — datasets look further from the framework than they are — and it put mnemonics
in the nearest-indicator column, where `VC VAW SXVLN` was being reported as a cluster's closest
SDG concept.

Excluding them moved every weak control up: Fortaleza from the 28th percentile to the 44th, Recife
from the 27th to the 32nd. The framework is now represented by its **519 named indicators**, and
the count is stated on the page rather than folded into a total.

Two smaller fixes in the same pass. Cluster examples were being spread one-per-city to show reach,
which made them unrepresentative of clusters dominated by one city — a cluster labelled for Italian
property valuations was illustrated with a Madrid shop register. Each cluster now shows its **most
central members** as well as the city spread. And the phrase view returns nothing here, which the
page now says is **expected by construction**: Spanish, Italian, Portuguese, German and Croatian
titles share essentially no bigrams.

## Where it stands

| | English | Non-English |
|---|---:|---:|
| Datasets / cities | 11,206 / 37 | 5,956 / 11 |
| Controls passing | 8 of 9 | **11 of 11** |
| Coherent clusters | 23 of 40 | 8 of 20 |
| Indicators nearest to nothing | 69 of 519 | 183 of 519 |

The non-English run has better controls and worse coverage — 183 indicators are nearest to no
dataset at all, against 69 in English, which is what you would expect from half the datasets and a
weaker cross-lingual model. It is not evidence that those cities publish less.
