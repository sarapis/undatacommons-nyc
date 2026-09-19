---
layout: default
title: "Correction: the platform names about 155 countries per call, not all but two"
author: Henry Grunzweig
date: 2026-09-19 12:30:00 -0400
---

[The 14 Sep post](https://sarapis.github.io/undatacommons-nyc/activity) said that "two countries
return empty names from `entityMetadata`" and fall back to their ISO codes. Two was the number
visible on one card. Measured across sixty calls, the platform names **152 to 162 places per
call** and returns an empty string for every place after that — and the places it drops are
always the **alphabetical tail by DCID**.

| Variable | Entities | Named | First unnamed |
|---|---:|---:|---|
| `undata/sdg/VC_IHR_PSRC` (homicide) | 198 | 154 | `country/SHN` |
| `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` | 185 | 158 | `country/SVK` |
| `undata/sdg/SH_STA_TRAF` (road deaths) | 195 | 162 | `country/SUR` |
| `undata/unicef/DM_POP` | 232 | 152 | `country/NIC` |
| `undata/sdg/EN_MWT_RCYR` (waste recycled) | 96 | 96 | — |

Sixty calls, thirty-three capped, and in every capped response no named place sorts after the
first unnamed one. The full table is
[`country-names-latest`](https://sarapis.github.io/undatacommons-nyc/artifacts/country-names-latest);
`python3 probe/country_names.py --check` re-measures it.

## What it was doing to us

Nothing in the response says a name was dropped, so a client that reads names off one call gets
South Africa, Sweden, Turkey, Ukraine, the United States and forty others as `''`.

- **`mcp/server.py`'s `world_position`** fell back to the DCID, so a neighbour could read
  `country/USA`. On the demo's homicide card 25 of 136 countries were blank; on road deaths, 33
  of 195; on PM2.5, 27 of 185. All on the S–Z end.
- **The 18 Sep smell test** carries no `place_name` on **563 of its 3,844 rows** — Malaysia
  through Zimbabwe — for the same reason. The written-up report was checked by hand and names
  every country, so nothing published to the platform team is affected; the artifact is.

## The fix is measured, not typed

A variable with fewer than ~150 reporting countries names all of them, so the tail is recoverable
from the platform itself. `probe/country_names.py` takes the union of names across calls, writes
`probe/cache/country_names.json`, and records the cap it observed on every call. **240 of the 246
places seen now carry a platform-supplied name.** The six that never do — `SGS`, `SJM`, `SXM`,
`UMI`, `VAT`, `VIR` — appear only in variables with more than 160 reporting places, so no call
ever reaches them; they print as ISO codes and the server lists them under `unnamed_places`.

`world_position` and `smell.py` now read live names first and fill from the cache, and the demo's
world strips are filled the same way (83 names; Vatican City remains `VAT`). `mcp/smoke.py`
fails if a neighbour is ever a bare DCID again, or if a nameable country on the demo is blank.

One more thing the same calls showed: **non-ASCII characters in names arrive as U+FFFD.**
`Curaçao`, `Réunion` and `Côte d'Ivoire` come back as `Cura�ao`, `R�union`, `C�te d'Ivoire`.
That is in the platform's response, not our decoding; it is cached as received.

## Why it matters beyond us

This is the fourth structural item for the platform team, after the 170 unnamed indicators, the
`Percent` unit, and `->relevantVariable` not being transitive. Every one of them has the same
shape: the response is well-formed, nothing errors, and the client cannot tell from outside that
it got less than it asked for. A response that named 155 of 198 places and *said so* would have
cost us nothing. One that says nothing cost a chart its labels for five days.
