---
layout: default
title: Inverse crosswalk — 2026-09-16
---

# The inverse crosswalk — 2026-09-16

Every other analysis here runs city → UN: take an SDG indicator, find the municipal dataset that matches it. That can only discover what the framework already asks about. This runs it backwards — take every dataset a city publishes, find its nearest SDG indicator, and look at what is left over.

**5,956 datasets** from **11 city portals** (language `non-en`), matched against **all 519 enumerated SDG indicators** — not the 442 with usable data, because a framework gap is a question about vocabulary rather than coverage.

**What a result here means.** A dataset far from every indicator means no SDG indicator's *text* is near this dataset's *text*. That is evidence about vocabulary, not proof of a conceptual gap — this project has already learned once that a null from the matcher is not evidence of absence. So the unit of evidence below is **how many independent cities** a theme appears in. A theme in thirty city catalogs is a category of municipal governance; a theme in one is that city's filing habit.

## Positive controls

Datasets from the hand-verified NYC crosswalk. These are known to correspond to an SDG indicator, so they must land in the high-affinity region. If they fall in the tail, the tail is measuring retrieval failure and nothing below is trustworthy.

**11 of 11 located · 0 fell in the tail.**

| Expected correspondence | City | Dataset | Affinity | Percentile | In tail? |
|---|---|---|---:|---:|---|
| Population structure (demographics) | Rostock | Bevölkerungsstruktur 2005 | 0.633 | 91 | no |
| Road traffic accidents (3.6.1) | Madrid | Accidentes de tráfico con implicación de b | 0.535 | 90 | no |
| Road traffic accidents and injuries (3.6.1) | Milan | Mobilità: incidenti stradali e persone inf | 0.516 | 90 | no |
| Municipal waste collected (11.6.1) | Milan | Rifiuti raccolti a Milano e nei comuni lim | 0.489 | 88 | no |
| Municipal waste collection (11.6.1) | Belo Horizonte | Coleta de Resíduos | 0.474 | 79 | no |
| Monthly road traffic accidents (3.6.1) | Matera | Bilancio mensile incidenti stradali anno 2 | 0.477 | 72 | no |
| Air quality, hourly (11.6.2) | Madrid | Calidad del aire. Datos horarios desde 200 | 0.462 | 71 | no |
| Water quality (6.3.2) | Buenos Aires | Calidad del Agua | 0.418 | 61 | no |
| Drinking water quality (6.1.1) | Karlsruhe | Jahresmittelwerte zur Trinkwasserqualität | 0.408 | 57 | no |
| Deaths from road traffic accidents (3.6.1) | Fortaleza | Número de Óbitos por Acidentes de Trânsito | 0.333 | 44 | no |
| Road traffic accidents with victims (3.6.1) | Recife | Acidentes de Trânsito com Vítimas 2016 | 0.394 | 32 | no |

## What cities publish that the SDGs have no words for

The bottom **25% of each catalog** by affinity — 1,516 datasets. Below are the title phrases that recur across that tail, **counted by how many independent cities use them**. These are not inferred categories; they are what the cities themselves called the data.

| Cities | Datasets | Phrase |
|---:|---:|---|

*No phrase recurs across four cities. Expected for a run pooling five languages — Spanish, Italian, Portuguese, German and Croatian titles share essentially no bigrams, so this view is uninformative here by construction rather than because nothing recurs. The clusters below carry the result.*

### In detail


## The same tail, clustered by embedding

A second view, kept because it groups datasets that share no vocabulary. k-means returns *k* clusters whether or not *k* themes exist, so each carries its **coherence** — the mean cosine of its members to its own centroid. Below 0.62, a cluster is a partition rather than a theme and is marked diffuse; **12 of 20 are.** Read those as noise, not as findings.

| Coherence | Cities | Datasets | Terms | Closest SDG indicator |
|---:|---:|---:|---|---|
| 0.895 | 6 | 241 | elezioni, sezione, risultati, referendum, abrogativo | Countries that have national urban policies  |
| 0.861 | 5 | 113 | omi, quotazioni, immobiliari, semestre, locazione | Performance index of data Infrastructure (Pi |
| 0.711 | 3 | 71 | orari, categoria, accessi, area, storica | Countries that have national urban policies  |
| 0.698 | 5 | 33 | telelavoro, personale, indeterminato, tempo, anno | Proportion of project objectives of new deve |
| 0.679 | 4 | 51 | pirf, zeis | Degree of implementation of integrated water |
| 0.676 | 2 | 51 | milanesi, accademico, universit, nelle, anno | Open Data Inventory (ODIN) Coverage Index |
| 0.644 | 7 | 39 | covid- | Number of new HIV infections per 1,000 uninf |
| 0.633 | 6 | 69 | ipem | Universal health coverage (UHC) service cove |
| 0.62 *(diffuse)* | 2 | 26 | geologia, sica, lote | Total greenhouse gas emissions (including la |
| 0.611 *(diffuse)* | 10 | 69 | (no term covers a fifth of this cluster) | Average proportion of Terrestrial Key Biodiv |
| 0.599 *(diffuse)* | 7 | 11 | kvaliteti, zraka, zagrebu, podaci, gradu | Carbon dioxide emissions per unit of GDP at  |
| 0.594 *(diffuse)* | 10 | 90 | (no term covers a fifth of this cluster) | Death rate due to road traffic injuries |
| 0.585 *(diffuse)* | 11 | 120 | (no term covers a fifth of this cluster) | Total public expenditure per capita on cultu |
| 0.557 *(diffuse)* | 9 | 72 | (no term covers a fifth of this cluster) | Proportion of municipal waste recycled |
| 0.552 *(diffuse)* | 7 | 70 | licita, fortaleza | Countries that have national urban policies  |
| 0.541 *(diffuse)* | 7 | 69 | zagreba, grada | Proportion of countries with alignment of Na |
| 0.535 *(diffuse)* | 4 | 35 | (no term covers a fifth of this cluster) | Countries that have national urban policies  |
| 0.51 *(diffuse)* | 7 | 34 | (no term covers a fifth of this cluster) | Countries that have legislative, administrat |
| 0.503 *(diffuse)* | 9 | 98 | (no term covers a fifth of this cluster) | Countries with procedures in law or policy f |
| 0.469 *(diffuse)* | 9 | 154 | (no term covers a fifth of this cluster) | Open Data Inventory (ODIN) Coverage Index |

### The coherent clusters in detail

**elezioni, sezione, risultati, referendum, abrogativo** — 241 datasets across 6 cities (coherence 0.895, mean affinity 0.294)

*Most central to the cluster:*

- Elezioni Politiche 1996 - Senato: Risultati di Sezione — Milan
- Elezioni Politiche 1996 - Camera - Quota Maggioritaria: Risultati di Sezione — Milan
- Elezioni Politiche 1996 - Camera - Quota Proporzionale: Risultati di Sezione — Milan
- Elezioni Comunali 2011 - Sindaco - Turno di ballottaggio: Risultati di Sezione — Milan
- Elezioni Comunali 2011 - Sindaco: Risultati di Sezione — Milan


*One per city, to show the spread:*

- Elezioni Europee 2019: Indirizzi e plessi elettorali — Milan
- Elecciones Autonómicas de la Comunidad de Madrid 4 de mayo 2021: colegios, callejero y mesas electorales — Madrid
- Resultado Concurso PBH Ativos 001/2018 — Belo Horizonte
- Partidos políticos reconocidos en CABA. — Buenos Aires
- Elezione diretta del Sindaco e del Consiglio Comunale della città di Matera 31 Maggio 2015 — Matera


**omi, quotazioni, immobiliari, semestre, locazione** — 113 datasets across 5 cities (coherence 0.861, mean affinity 0.32)

*Most central to the cluster:*

- Quotazioni Immobiliari OMI: Locazione - Semestre 2004/1 — Milan
- Quotazioni Immobiliari OMI: Locazione - Semestre 2004/2 — Milan
- Quotazioni Immobiliari OMI: Compravendita - Semestre 2014/1 — Milan
- Quotazioni Immobiliari OMI: Compravendita - Semestre 2014/2 — Milan
- Quotazioni Immobiliari OMI: Compravendita - Semestre 2004/1 — Milan


*One per city, to show the spread:*

- Quotazioni Immobiliari OMI: Compravendita - Semestre 2021/2 — Milan
- Concesiones de quioscos — Madrid
- BASE DE DADOS DA SUBPREFEITURA M'BOI MIRIM 2026 — São Paulo
- Seguimiento de Obras Adjudicadas (SOA). — Buenos Aires
- Elenco Farmacie — Matera


**orari, categoria, accessi, area, storica** — 71 datasets across 3 cities (coherence 0.711, mean affinity 0.306)

*Most central to the cluster:*

- AREA C: accessi orari 2012 distinti per veicoli di servizio — Milan
- Parco veicolare, suddiviso per categoria - Serie storica — Milan
- AREA C: accessi orari 2014 distinti per veicoli di servizio — Milan
- AREA C: accessi orari 2014 suddivisi per categoria veicolo — Milan
- AREA C: accessi orari 2015 distinti per veicoli di servizio — Milan


*One per city, to show the spread:*

- Parco veicolare circolante: consistenza, immatricolazioni e radiazioni - serie storica — Milan
- Mapa Altimétrico 2015 — Belo Horizonte
- Trasporti Pubblici Locali Comune di Matera - GTFS — Matera
- ATM - Orari linee di superficie urbane — Milan
- ATM - Orari linee metropolitane — Milan


**telelavoro, personale, indeterminato, tempo, anno** — 33 datasets across 5 cities (coherence 0.698, mean affinity 0.316)

*Most central to the cluster:*

- Personale a tempo indeterminato in Telelavoro - anno 2018 — Milan
- Personale a tempo indeterminato in Telelavoro - anno 2014 — Milan
- Personale a tempo indeterminato in Telelavoro - anno 2019 — Milan
- Personale a tempo indeterminato in Telelavoro - anno 2021 — Milan
- Personale a tempo indeterminato in Telelavoro - anno 2017 — Milan


*One per city, to show the spread:*

- Inail: infortuni sul lavoro denunciati dalle aziende - Suddivisione per genere — Milan
- Mentoring — Madrid
- Centros de Jubilados — Buenos Aires
- Popolazione Scolastica Istruzione Inferiore Pubblica di Matera A.S. 2014-2015 — Matera
- Kindertagesbetreuung — Karlsruhe


**pirf, zeis** — 51 datasets across 4 cities (coherence 0.679, mean affinity 0.261)

*Most central to the cluster:*

- PIRF ZEIS Pici - Prop. Equipamentos - Zeis Pici — Fortaleza
- PIRF ZEIS Pici - Prop. Espaços Livres - Zeis Pici — Fortaleza
- PIRF ZEIS Pici - Vazios Subutilizados - Zeis Pici — Fortaleza
- PIRF ZEIS Pici - Espaços Livres - Zeis Pici — Fortaleza
- PIRF ZEIS Pirambu - Alargamento  - Zeis Pirambu — Fortaleza


*One per city, to show the spread:*

- Plano Básico de Zona de Proteção de Helipontos  - PBZPH — Fortaleza
- Servidores cedidos para PBH — Belo Horizonte
- PSTDA - SUB CAMPO LIMPO — São Paulo
- Raskrižja sa zvučnim signalizatorima — Zagreb
- PDA SMS — Fortaleza


**milanesi, accademico, universit, nelle, anno** — 51 datasets across 2 cities (coherence 0.676, mean affinity 0.312)

*Most central to the cluster:*

- Iscritti nelle Università Milanesi Anno Accademico 2010-2011 — Milan
- Iscritti nelle Università Milanesi Anno Accademico 2011-2012 — Milan
- Immatricolati nelle Università Milanesi Anno Accademico 2017-2018 — Milan
- Immatricolati nelle Università Milanesi Anno Accademico 2010-2011 — Milan
- Immatricolati nelle Università Milanesi Anno Accademico 2016-2017 — Milan


*One per city, to show the spread:*

- Open Wifi Milano: Utenti unici giornalieri per zona — Milan
- Audit Dataset — Fortaleza
- Istruzione: Scuole dell'infanzia - unità scolastiche, classi e alunni per municipio e tipologia di gestione (a.s. 2002/2003-2023/2024) — Milan
- Istruzione: Scuole primarie - unità scolastiche, classi e alunni per municipio e tipologia di gestione (a.s. 2002/2003-2023/2024) — Milan
- Istruzione: Scuole secondarie di I grado - unità scolastiche, classi e alunni per municipio e tipologia di gestione (a.s. 2002/2003-2023/2024) — Milan


**covid-** — 39 datasets across 7 cities (coherence 0.644, mean affinity 0.307)

*Most central to the cluster:*

- Llamados 107 COVID-19 — Buenos Aires
- Casos Graves – Covid-19 — Recife
- Casos Leves – Covid-19 — Recife
- Tos COVID-19 — Buenos Aires
- Casos COVID-19 — Buenos Aires


*One per city, to show the spread:*

- COVID-19. Intervenciones del Cuerpo de Bomberos — Madrid
- Transparência - Servidores 2020 — Fortaleza
- Contratos Covid-19 — Belo Horizonte
- Execução Orçamentária - COVID-19 — São Paulo
- Reporte COVID-19.. — Buenos Aires


**ipem** — 69 datasets across 6 cities (coherence 0.633, mean affinity 0.273)

*Most central to the cluster:*

- Verificações Ipem 04/2023 — Fortaleza
- Produtos Pré-medidos 04/2023 — Fortaleza
- Verificações Ipem 02/2023 — Fortaleza
- Execução Ipem 04/2023 — Fortaleza
- Produtos Pré-medidos 02/2023 — Fortaleza


*One per city, to show the spread:*

- Elecciones Asamblea de Madrid 1983-2023 — Madrid
- Relatório Quantitativo de Ouvidoria 2024 — Fortaleza
- Coeficiente CN Cenário 2021 — Belo Horizonte
- DICIONÁRIO DE DADOS DA SUBPREFEITURA M'BOI MIRIM 2026 — São Paulo
- Elecciones 2023 — Buenos Aires



## Reproducing

```bash
python3 probe/fetch_municipal.py
python3 probe/inverse.py
```

