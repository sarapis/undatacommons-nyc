---
layout: default
title: A category with no indicator — electoral data — 2026-09-16
---

# A category of city data the SDG framework has no words for

**For the UN System Data Commons platform team.** Prepared 16 Sep 2026 by the NYC Voluntary Local
Review team (Builders' Day participants). This is **not a defect report** — nothing here is broken.
It is an observation about what the graph can and cannot represent, found while building a
city↔UN indicator crosswalk, and it bears directly on the question we most want to ask you: *is
there a sanctioned path for a city to contribute a series?*

We should be precise about ownership. The SDG indicator framework is set by the UN Statistical
Commission and the IAEG-SDGs, not by this platform. What follows is not a request to change it.
It is a measurement of a gap between what the framework asks and what cities actually publish,
offered because it bounds what municipal data could ever be ingested here.

---

## The finding in one line

**Zero of the 519 named SDG base indicators mention elections, voting or turnout. Twenty-three
cities publish 469 datasets that do.**

## How the zero was established

We enumerated the SDG goal framework by walking `->relevantVariable` from the seventeen goal
roots: **689 base indicators**. Of those, 519 return a name; the other 170 return none (see the
second section below). Searching all 519 names for `election | electoral | vote | voter | voting |
turnout | ballot | referendum | suffrage | polling | candidate` returns **nothing**.

We also checked the 170 unnamed DCIDs by mnemonic. Two look electoral and neither is:

| DCID | What it is |
|---|---|
| `undata/sdg/SE_ACS_ELECT` | The SDG series code for *schools with access to **electricity*** (4.a.1) — `SE_` is the education prefix |
| `undata/sdg/SG_SCP_POLINS` | Sustainable-consumption **policy instruments**, not political institutions |

Neither returns a name from `get_variable_metadata`, so we could not confirm either from the graph
itself and are inferring from the series-code convention. If either is in fact electoral, this
finding weakens and we would want to know.

**What the framework does measure nearby**, and why none of it covers the gap:

| Indicator | What it captures |
|---|---|
| `SG_GEN_PARLNT` — current number of seats in national parliaments | The size of the elected body |
| `SG_DMK_PARLMP_LC/_UC` — female representation ratio in parliament | The **composition** of the elected body (SDG 5.5.1) |
| `IU_DMK_INCL` / `IU_DMK_ICRS` — proportion who **believe** decision-making is inclusive | A perception survey (SDG 16.7.2) |
| `SG_GOV_LOGV` — number of local governments | A count of entities |

So the framework counts seats, measures who occupies them, and asks people how they feel about it.
**Nothing measures the conduct of an election**: turnout, results, polling-station distribution,
ballot accessibility, electoral register coverage.

## What the cities publish

Scanning **17,162 datasets across 48 municipal portals** for electoral vocabulary in the title, in
six languages:

- **469 datasets, across 23 cities and 23 portals.**
- **64% of them fall in the bottom quartile of their own catalog** by similarity to any SDG
  indicator — measurably further from the framework than the average municipal dataset (mean
  affinity **0.332** against **0.407** for all datasets).

| City | Datasets | Examples |
|---|---:|---|
| Milan | 310 | *Elezioni Politiche 1996 – Senato: Risultati di Sezione*; polling-station results by section, continuously since 1996 |
| Edmonton | 35 | *2017 Official Election Results (by Voting Station)* |
| Calgary | 27 | *Official Results – General Election 2021 – Senate* |
| Los Angeles | 15 | *Election 2015 May General Voting Results* |
| Cambridge, MA | 13 | *2016 Presidential and State Election Results* |
| Winnipeg | 13 | *Council Voting Data* |
| New York | 10 | *Voting/Poll Sites* |
| Madrid | 9 | *Elecciones Autonómicas 2021: colegios, callejero y mesas electorales* |
| Buenos Aires | 9 | *Partidos políticos reconocidos en CABA* |
| Matera | 2 | *Elezione diretta del Sindaco e del Consiglio Comunale, 31 Maggio 2015* |
| Karlsruhe | — | *Europawahl 2019* |
| …12 more | | Chicago, Boston, Austin, Baton Rouge, Somerville, Dallas, Oakland, New Orleans, Santa Monica, Everett, Cincinnati, Orlando, Recife |

**Milan alone is 66% of the datasets**, so the dataset count is not evidence of breadth. The city
count is: excluding Milan entirely leaves **159 datasets across 22 cities**, which is the number
this finding actually rests on.

## The most telling detail

For each electoral dataset we recorded which SDG indicator the matcher ranked closest. The six most
common answers across all 469:

| Times | Nearest SDG indicator |
|---:|---|
| 70 | Countries that have national urban policies or regional development plans… |
| 61 | Countries that adopt and implement…guarantees for public access to information |
| 42 | Current number of seats in national parliaments |
| 36 | Countries with national statistical plans with funding from government |
| **35** | **Municipal waste collected** |
| 34 | Extent to which global citizenship education…is mainstreamed |

For thirty-five municipal election datasets, the closest concept in the entire SDG framework is
**municipal waste collected**. That is not a failure of the matcher so much as a description of the
space it is searching.

## Corroboration

The same category surfaced independently in two runs that share no cities and no embedding model:

| | English run | Non-English run |
|---|---|---|
| Model | `potion-base-32M` | `potion-multilingual-128M` |
| Cities in the cluster | 10 — Baton Rouge, Boston, Calgary, Cambridge, Chicago, Edmonton, Los Angeles, New Orleans, New York, Winnipeg | 6 — Belo Horizonte, Buenos Aires, Karlsruhe, Madrid, Matera, Milan |
| Datasets / cluster coherence | 57 / 0.71 | 241 / **0.90** — the tightest cluster in the whole analysis |
| Nearest indicator the cluster resolved to | *Number of local governments* | *Countries that have national urban policies…* |

Two disjoint sets of cities, two different models, one category.

## Limits, stated

- **This is a vocabulary result, not a conceptual proof.** A dataset far from every indicator means
  no indicator's *text* is near its *text*. We hold this to be evidence of a framework gap only
  because it recurs across 23 independent cities; a single city's filing habit would prove nothing.
- **Our matcher's precision is roughly half** on hand-read candidate lists, and one positive
  control in nine fell into the tail in the English run (NYC's *Housing Maintenance Code
  Violations*, a hand-verified match for 11.1.1, at the 21st percentile). The tail contains real
  matches.
- **The English cluster mixes two things**: municipal elections and council roll-call votes
  (Winnipeg's *Council Voting Data*, Calgary's *Council and Committee Votes*). Both are democratic
  process; only the first is an election.
- Full method and every caveat: [inverse crosswalk](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-latest)
  and [the non-English run](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-non-en-latest).

---

## A second item, which *is* yours

**170 of the 689 enumerated SDG base indicators return no name.** `get_variable_metadata` answers
for them but the `name` field is absent, and they return no observations either — so from outside
there is no way to tell what `DI_ILL_OUT`, `EN_BITR_REP_DV` or `SE_ACS_ELECT` measure.

It is a quarter of the enumerated framework, and it has a direct cost for anyone building on the
graph: our first matching run fell back to the DCID mnemonic as query text, so a quarter of "the
framework" was represented by strings like `DI ILL OUT`, against which nothing can match. That
inflated our gap measurements until we excluded them. We now match against the 519 named
indicators and say so on the page.

A name on those 170 would fix it. It is also what stopped us confirming the two electoral-looking
mnemonics above.

Sample: `AG_FPA_COMM`, `DI_ILL_IN`, `DI_ILL_OUT`, `EN_ATM_CO2MVA`, `EN_BITR_REP`, `EN_BITR_REP_DV`,
`EN_HAZ_TREATV`, `EN_LKW_QLTRB`, `EN_LKW_QLTRST`, `EN_LND_SLUM`, `EN_MAR_BEALIT_BV`,
`EN_MAR_CHLANM`. The full list is in
[the inverse crosswalk artifact](https://sarapis.github.io/undatacommons-nyc/artifacts/inverse-latest).

---

## Why we are raising it

Our project is a live Voluntary Local Review workbench: NYC series mapped to UN indicator DCIDs
with a comparability grade on every mapping. Everything we have built runs city → UN, which can
only ever surface what the framework already asks about. Running it backwards is how this appeared.

If city-level contribution is on the roadmap, then the categories cities *actually* publish — and
electoral administration is among the largest and most consistent of them — are the ones that will
have nowhere to land. We would be glad to discuss it at Builders' Day on 22 September.

## Reproducing

```bash
git clone https://github.com/sarapis/undatacommons-nyc
python3 probe/fetch_municipal.py
python3 probe/inverse.py                    # English catalogs
python3 probe/inverse.py --language non-en  # the other five languages
```
