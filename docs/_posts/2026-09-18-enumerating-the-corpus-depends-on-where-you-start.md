---
layout: default
title: "Enumerating the corpus depends on where you start"
author: Devin Balkind
date: 2026-09-18 16:20:00 -0400
---

Every count this project publishes rests on one number: **689 base indicators**, enumerated by
walking `->relevantVariable` from the seventeen SDG goal trees. Ran the same walk from the graph's
actual root to see what else is there.

| | From the 17 SDG goal trees | From `undata/topic/Root` |
|---|---:|---:|
| Topic nodes | 3,761 | **29,805** |
| Peer groups | 1,916 | **19,532** |
| Variables | 6,025 | **65,418** |
| Base indicators | 689 | **1,661** |

**978 base indicators are unreachable from the SDG goal framework** — WHO 354, UNICEF 245, ILO 93,
UNIDO 69, UNAIDS 41, OHCHR 36, UNFPA 32, UNDP-HDRO 28, ITU 25, UNESCO 18, UNODC 12, ECLAC 6,
UNDRR 5, IOM-DTM 1, UNHCR 1. The goal framework is **41%** of the governed corpus.

## The part worth reporting

Six base indicators are reachable from the goal trees and **not** from Root:

```
undata/sdg/SG_DSR_SILN   undata/sdg/VC_DSR_AGLH
undata/sdg/SG_DSR_SILS   undata/sdg/VC_DSR_CHLN
undata/sdg/SM_POP_REFG_OR  undata/sdg/VC_DSR_HOLH
```

All seventeen goal trees are **direct children of Root** — we checked, they are 17 of its 42
children. So a traversal from Root should be a strict superset of a traversal from the goal trees,
and it is not.

Three things rule out the boring explanations:

- **Neither walk reported a single fetch error.** The walker prints and retries on failure; the
  logs are clean.
- **The goal-tree walk is exactly reproducible.** Re-run two days later it returned 689 again, the
  identical set. This is not run-to-run noise.
- **The disagreement runs both ways.** Twelve `undata/sdg/` indicators are reachable from Root and
  not from the goal trees — the youth-in-parliament series `SG_DMK_PARLYTH*` and the global
  citizenship education series `SE_SGE_*` among them.

So `->relevantVariable` is not transitive across these hierarchies, and **no single entry point
enumerates the graph completely**. A client that picks one — as we did, for principled reasons —
gets a silently incomplete corpus and no way to know it. That is worth the platform team knowing,
and it is the third structural item we have for them, after the 170 unnamed indicators and the
`Percent` unit covering both bounded proportions and signed rates.

## What it does not change

**The 689 is still the right denominator for this project, and nothing published needs correcting.**
A Voluntary Local Review reports against the SDG goal framework; enumerating from those seventeen
trees is the correct scope, not a shortcut. The demo's masthead says "689 base indicators in the
goal framework", which is exactly what it is.

What changes is that we now know the framework's share: 689 of 1,661, and the other 978 are the
agency series — WHO's health indicators, ILO's labour series, UNICEF's child statistics — which a
city might well want and which no SDG-scoped enumeration will ever surface.

## Next

The smell test is running against the 978 now. The first twenty-five rows already show ILO series
with 1,067 and 1,471 observations across 135 countries, so this is not a thin surface. All five
data errors found so far came from `undata/sdg/` alone, which was 41% of the graph; this is the
other 59%.

`probe/corpus.py --roots all` now writes to its own file and keeps its own resume state, so a
whole-graph walk can no longer overwrite the SDG corpus that every downstream count resolves
against. It would have, silently, before today.
