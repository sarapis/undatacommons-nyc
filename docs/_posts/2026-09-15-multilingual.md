---
layout: default
title: "Multilingual embeddings: Madrid 0 → 19, Milan 0 → 5, and a trade-off we kept"
author: Devin
date: 2026-09-15 23:30:00 -0400
---

The blocker for every non-anglophone city was the embedding model, not the pipeline. Adding
`potion-multilingual-128M` unblocks them — and measuring it showed the fix is not free.

| City | Lang | Before | After | Best sim |
|---|---|---:|---:|---:|
| Madrid | es | 0 | **19** | 0.59 |
| Milan | it | 0 | **5** | 0.67 |

## Why it is not a straight swap

On the seven hand-verified NYC pairs, against the full 2,400-dataset catalog:

| Model | Median rank | top-10 | top-50 |
|---|---:|---:|---:|
| `potion-base-32M` (English) | **23** | 3/7 | **5/7** |
| `potion-multilingual-128M` | 81 | 3/7 | 3/7 |

Swapping wholesale would have bought non-English coverage with English accuracy — a 3.5× worse
median rank on the catalog we know best. Interestingly it is not uniform: the multilingual model
*improves* the two hardest cases (homicide 786→401, slums 1033→716) while degrading the easy ones.

So the model is chosen **per catalog language**. English cities keep the English model; everything
else gets the multilingual one. The vector cache is keyed by model, because vectors from two
models are not interchangeable and reusing them across would be a silent, invisible corruption.

## The matches, read honestly

**Milan is good** — 4 of 5 plausible:

- *Annual inflation (consumer prices)* → **Tasso di inflazione mensile** (0.60)
- *Installed renewable electricity capacity* → **Produzione netta di energia elettrica** (0.67)
- *Energy intensity of primary energy* → **Energia elettrica erogata da A2A** (0.60)

**Madrid is noisy** — six near-identical "water area of lakes and rivers" indicators all matched
**Fuentes de agua para mascotas**, drinking fountains for pets. The word *agua* dominated. But
buried in the noise: *installed renewable capacity* → **Inventario de instalaciones fotovoltaicas**,
which is exactly right.

The threshold problem is language-independent: 0.50 was calibrated on NYC and means something
different in every other catalog. That remains the open issue, and it is now the main thing
standing between this and a usable recommender.

## Buenos Aires is unreachable, not empty

The portal closes the connection on anonymous `package_search` — `RemoteDisconnected`, on two
attempts a day apart. Recorded in the registry as `status: unreachable` rather than as zero
candidates, because those are different findings and collapsing them would overstate what we
tested.
