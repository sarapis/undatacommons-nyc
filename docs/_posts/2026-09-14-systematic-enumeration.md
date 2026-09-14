---
layout: default
title: "Systematic enumeration: 689 SDG indicators, 248 with US data, and a matcher that is only a third right"
author: Devin
date: 2026-09-14 09:00:00 -0400
---

The first eleven crosswalk pairs came from topics I chose out of my head, which meant the
crosswalk could only ever confirm my assumptions about NYC's data. This replaces that with a
three-stage pipeline driven by the UN corpus.

```bash
python3 probe/corpus.py      # enumerate  -> 689 base SDG indicators
python3 probe/screen.py      # US coverage -> 248 GREEN
python3 probe/match_nyc.py   # NYC candidates -> ranked shortlist
```

## The denominator

**689 base SDG indicators.** The eleven hand-picked pairs were 1.6% of it.

| Screen | Count |
|---|---:|
| GREEN — usable US series | **248** |
| AMBER | 37 |
| RED | 27 |
| NO-US-DATA | **377** |

55% of SDG indicators have no US data at all. The real candidate pool is 248, of which my
hand-picking sampled 4%.

## Two traps in the platform worth knowing

**The goal trees do not expose variables.** Walking `sdgf/goal-*` yields `undata/svpg/...` nodes
— StatVarPeerGroups — which carry no observations. The tempting move is rewriting
`svpg/sdg/X` to `sdg/X`, which looks right and is precisely the DCID guessing the platform
forbids. The correct path is following each group's `->member` arc. Verified the svpg nodes
return nothing before building on them.

**`get_variable_metadata` silently truncates above ~10 variables per call** — `status: None` and
an empty map, not an error. The first screening run used batches of 40 and reported
"screened 689/689" having actually recorded **nine**. Now capped at 10, with any short response
treated as failure and re-split, and anything the graph never returned reported explicitly.

That is the third time on this project that every automated check passed and the number was
still wrong. It keeps being the same lesson.

## The matcher is the weak link, and it should be said plainly

First run produced mostly false positives. Short indicator names have few keywords, so one
coincidental word scored 1.0:

- *Number of local governments* → **EEO-4 Reports**
- *Secure tenure rights to land* → **City Council September Attendance Report**
- *Domestic material consumption* → **Mayor's Office to End Domestic Violence**

Tightened two ways: a match now needs at least two distinct indicator terms rather than high
proportional coverage alone, and inherently national indicators (balance of payments, ODA,
tariffs, treaties, fisheries) are excluded before searching, since a city does not publish them
and matching could only manufacture noise.

Result: 248 GREEN → 73 not city-scoped → **43 with candidates, 39 not yet in the crosswalk.**
Roughly a third of those look plausible on inspection. Term overlap is a genuinely poor proxy
for semantic equivalence and no amount of tuning will fix that; the output is labelled a
shortlist for human review and should be read as nothing more.

## What it surfaced that I would never have picked

- **CO2 emissions from fuel combustion** (`EN_ATM_CO2`, 24 obs) against NYC's Climate Budgeting
  emission factors.
- **Energy intensity of primary energy** (`EG_EGY_PRIM`, 34 obs) against Local Law 84 building
  energy benchmarking — an area where NYC's data is unusually strong.
- **Government spending on essential services** (`SG_XPD_ESSRV`, 24 obs) against Agency Spending
  by Budget Function.

Those are the pipeline earning its keep. None were on my list.

## Next

The honest improvement is not more scorer tuning. It is using a real embedding model against
NYC dataset titles instead of my keyword overlap — the platform already does this properly for
its own search, and I am reimplementing it badly.
