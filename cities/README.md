# Multi-city bootstrapping

Generalises the NYC pipeline to any city in `registry.json`, over Socrata **or** CKAN.

```bash
python3 probe/bootstrap.py --city boston
```

## It does not produce a crosswalk, and cannot

Comparability spec v0.1 says a grade is a human judgment. A machine emitting a "crosswalk" would
violate the spec this project publishes. The output is `candidates.json` with
`is_crosswalk: false` — the worksheet a local analyst grades, not a result.

## What the first run found — mostly a negative result

| City | Platform | Lang | Datasets | Field names | Candidates | Best sim |
|---|---|---|---:|---:|---:|---:|
| Chicago | socrata | en | 915 | 915 | 6 | 0.55 |
| Boston | ckan | en | 235 | 0 | 7 | 0.57 |
| San José | ckan | en | 170 | 0 | 4 | 0.58 |
| Madrid | ckan | es | 672 | 0 | **0** | 0.27 |
| Milan | ckan | it | 2602 | 0 | **0** | 0.29 |
| Buenos Aires | ckan | es | — | — | — | portal dropped the connection |

**The plumbing generalises. The matching does not.**

### 1. Cross-language matching fails completely

Not degradation — failure. Madrid tops out at **0.265** and Milan at **0.294**, against Boston's
0.575. Medians are 0.15–0.18, which is noise. Milan has a *larger* catalog than NYC and matches
nothing. Lowering the threshold would admit garbage, not signal: Madrid's single best match pairs
*carbon dioxide emissions per unit of GDP* with *municipal parking permit lists*.

The embedding model is English-only. A multilingual model is the fix; there is no tuning around it.

### 2. Field names were not the problem — a hypothesis we had wrong

We predicted CKAN cities would be handicapped because CKAN does not publish column names in its
catalog API and Socrata does. Chicago publishes field names on **915 of 915** datasets and found
*fewer* candidates than Boston, which publishes **none**. The hypothesis is dead.

### 3. The similarity threshold does not transfer between catalogs

0.50 was calibrated against NYC's 2,400-dataset catalog. In a smaller catalog the nearest
neighbour is simply whatever is least unrelated, so the same number admits nonsense: Boston's
top-scoring match pairs *Food waste* with *Trash Schedules by Address* at 0.57.

Reviewing all 13 English-city candidates by hand, roughly **2–3 per city are plausible** — and
**not one substantive SDG indicator matched in any city.** No air quality, no homicide, no waste
tonnage, no road deaths. What matched was generic budget, land and performance vocabulary that
shares words with indicator names.

## What would actually fix it

1. **A multilingual embedding model** — unblocks every non-English city, which is most of them.
2. **Per-catalog threshold calibration** — an absolute cosine score has no fixed meaning across
   catalogs; a percentile or a margin over the catalog's own distribution would.
3. **Human search as the primary path**, with the matcher demoted to a hint. NYC's good pairs were
   found by a person who knew the data; the matcher confirmed them.

Until at least (1) and (2), treat this as infrastructure with a known-poor recommender attached.
