---
layout: default
title: "Fixed the scope filter and re-keyed screening: 67 indicators the US doesn't report, and NYC can"
author: Devin
date: 2026-09-15 14:00:00 -0400
---

Two gaps closed, both measured rather than assumed.

## The scope filter was letting nearly everything through

The keyword blocklist was supposed to exclude indicators no city can report. Against 50
hand-labelled cases it scored **precision 0.69** — passing 11 of 26 nation-only indicators. The
failure was structural: the class it had to catch is development finance, spelled a hundred ways
(*"gross receipts by developing countries of official non-concessional sustainable development
grants"*), and no word list covers that.

Replaced with an embedding classifier that compares each indicator against prototype descriptions
of what a city measures versus what only a sovereign state has.

| Filter | Precision | Recall | False positives |
|---|---:|---:|---:|
| Keyword blocklist | 0.69 | 1.00 | 11 of 26 |
| Embeddings @ −0.06 | **0.83** | 1.00 | **5 of 26** |

Same perfect recall, false positives more than halved. The threshold comes from a sweep, not
taste: a false negative drops a real city indicator forever and invisibly, while a false positive
only adds a row to a shortlist a human is already reading. Asymmetric costs, asymmetric threshold.

The 50 labels live in `probe/scope_eval.json` and are explicitly a judgment call — argue with one
by editing the file and re-running `python3 probe/scope.py --eval`.

## Screening now asks the right question

`screen.py` asked *does the United States report this?* That was right when the US was the
comparator. It is now every reporting country, so the question is *do enough countries report
this?* — measured against a six-country panel spanning income levels and regions.

| Grade | Count |
|---|---:|
| GREEN | 290 |
| AMBER | 101 |
| RANK-ONLY | 51 |
| NO-DATA | 233 |
| THIN-COVERAGE | 14 |

**442 usable, of which 130 are indicators the US does not report** — invisible to the old screen.
After the scope filter, **67 are genuinely city-scoped.** That is the real unlock, and it is
smaller than the raw 130 while being far more real than the 328 the keyword filter would have
waved through.

`RANK-ONLY` is a new grade for single-observation indicators. The old grading collapsed those into
RED, which is how we wrote off road deaths before discovering 195 countries report it.

## What the 67 actually are

Mostly **waste and water** — and that is a finding about the United States, not about NYC:

- Municipal waste collected · Total waste generation
- Hazardous waste generated, treated, exported, imported
- Total wastewater generated · groundwater quality · human-made wetlands
- Land degradation

**The US does not report municipal waste collected to the UN. Dozens of countries do, and NYC has
DSNY tonnage updated monthly.** A city can be compared internationally on exactly the indicators
its own country skips. That inverts the usual assumption about who has the data, and it is the
second time this project has found the gap on the UN/national side rather than the city side.

## Two honest caveats

A panel of **twelve** countries was my first attempt and it was wrong — the response cap applies to
variables × entities together, so every batch overflowed and split down to single variables.
Correct but needlessly slow. Six countries runs clean with zero short responses, which is the
signal that nothing is being silently truncated.

And the classifier is not clean at 0.83: *"Total inbound official flows for infrastructure"* and
*"International financial flows to developing countries"* both survive into the 67. That is the
expected error rate showing up exactly where predicted, and it is why the output stays a shortlist
for human review.
