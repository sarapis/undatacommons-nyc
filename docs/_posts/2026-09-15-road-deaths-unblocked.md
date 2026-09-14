---
layout: default
title: "Road deaths unblocked: NYC is 18th of 196, and the blocker was our framing"
author: Devin
date: 2026-09-15 09:30:00 -0400
---

We graded road deaths **BLOCKED** because the UN holds one observation for the United States.
That is true of a trend and irrelevant to a ranking: WHO publishes a single global round, and in
2021 **195 countries reported**. One year is more than enough to place a city.

The blocker was our framing, not the data.

## The result

**NYC: 297 road deaths in 2021, 3.51 per 100,000 — 18th of 196.**

| | per 100k |
|---|---:|
| Germany | 3.30 |
| Netherlands | 3.40 |
| Spain | 3.50 |
| **New York City** | **3.51** |
| Cyprus | 3.90 |
| *United States* | *14.20* |

NYC's streets are as safe as Western Europe's and roughly **four times safer than the country it
sits in**. That finding was completely invisible while the comparator was the US — which is the
best argument yet for the world view existing at all.

## The card puts one line beside one dot

NYC's eleven years of rates and the UN's single 2021 observation share one axis. The asymmetry is
the argument: a dense blue line running low and flat, and a lone orange dot four times higher.

The grade is new — **RANK ONLY**. Not blocked, not chartable as a trend. NYC can be *placed*
among 195 countries and cannot be *tracked* against them, because the world has one snapshot and
NYC has eleven years. The inversion panel now says that instead of claiming the comparison fails.

## A bug worth owning

The first version drew NYC's line straight **through** 2020 while annotating "no ACS 2020" beside
it. The series omitted 2020 rather than carrying an explicit null, so the line bridged the gap.
The homicide chart already broke correctly.

On a page whose entire argument is that missing data should stay visible, that was the wrong bug
to ship. Fixed: an explicit null, a real break.

## What else the world view opens, honestly

- **Drinking water** stops being flat — 162 countries, real variation. Still low value for a NYC
  analyst, so it stays excluded, with the reason corrected.
- **The other six blocked pairs stay blocked.** Mismatched age bands, a denominator in another
  dataset, the international poverty line, share-versus-count, no NYC source. Those are
  definitional; more countries cannot fix them.
- **The 377 NO-US-DATA indicators look like a doubling and are not.** They are overwhelmingly
  ODA, debt service, climate finance and "gross receipts by developing countries" — the US does
  not report them because it is a donor, and a city cannot report them either. Our city-scope
  filter passes 328 of the 377, so it is far too weak to catch that class. That is a real gap in
  the pipeline, not a finding about the data.

The screening criterion should change too: `screen.py` asks *does the US report this?* when the
comparator is now the world. The right question is *do enough countries report it?*
