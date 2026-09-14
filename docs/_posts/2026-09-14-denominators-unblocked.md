---
layout: default
title: "Denominators wired: all three pairs chartable, and NYC's homicide rate crossed below the US in 2013"
author: Devin
date: 2026-09-14 21:00:00 -0400
---

Census key in hand, so the denominator problem is solved and every Tier 3 rate indicator is
unblocked, not just homicide. All three crosswalk pairs now resolve end to end.

## The homicide comparison

NYC counts murders; the UN publishes a rate per 100,000. With ACS annual population as the
denominator, the two finally share an axis — and the result is a real finding:

| Year | NYC | US |
|---|---:|---:|
| 2006 | 6.93 | 5.79 |
| 2010 | 6.50 | 4.73 |
| 2013 | 3.83 | 4.47 |
| 2017 | 3.22 | 5.21 |
| 2021 | 5.62 | 6.78 |
| 2023 | 4.66 | 5.76 |

**NYC crossed from above the national homicide rate to below it around 2013, and stayed below
through the 2021 spike.** That is the kind of statement a city analyst can actually use, and it
is invisible from either dataset alone.

## The 2020 hole is real and we are leaving it

There is **no ACS 1-year release for 2020** — the Bureau withheld the standard product after
COVID disrupted collection. So 2020 has no denominator, and therefore no rate.

2020 is the year NYC homicides jumped to 456. The gap lands precisely on the most interesting
year in the series.

We leave it empty. An interpolated denominator produces a rate that is visually
indistinguishable from a measured one, and this is exactly the case where someone would quote it.
The probe records dropped years explicitly rather than silently omitting them. 2025 is also
absent for the ordinary reason that the vintage is not published yet.

## Secret handling

The Census key lives in a gitignored `.env` and is read from the environment. It is in **no**
tracked file and **no** commit — verified against the full history, not just the working tree.
This repo is public and its parent workspace has a live incident from committed keys, so the
check is deliberate rather than assumed.

Collaborators: get your own free key at <https://api.census.gov/data/key_signup.html> and export
`CENSUS_API_KEY`. The probe explains this if the key is missing.
