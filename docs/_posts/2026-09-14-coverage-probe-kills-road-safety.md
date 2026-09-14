---
layout: default
title: "Coverage probe: road safety is out, homicide and waste are in"
author: Devin
date: 2026-09-14 11:00:00 -0400
---

Built the coverage probe harness and ran it across 15 candidate topics. It sweeps indicators,
pulls each full series, and grades them on whether they can actually carry a chart. First run:
**30 GREEN, 9 AMBER, 5 RED**.

**Road safety is dead as our headline demo.** All three road-traffic variables came back RED with
a single observation each — SDG 3.6.1 has exactly one US data point, 2021. That was the worked
example in our application. Better to find out now than at 4pm on demo day, which is the whole
reason the harness exists.

The replacements are stronger anyway. **Homicide rate** (16.1.1) has 21–31 annual points back to
1990 and NYC publishes closely matching data. **Municipal waste recycled** (11.6.1) has 19 points
and pairs naturally with the DSNY diversion rate. Renewable energy share and unemployment are
both dense too.

The genuinely interesting find: several variables carry an `URBANIZATION--DOU_CITY` slice, e.g.
`undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY`. It is a national figure cut by degree of
urbanization — "the city parts of the US", not any particular city — but it may be the most
honest comparator available for a NYC number, and it partially softens the no-city-data finding.
Worth an hour before we commit to a framing.

Two limitations, documented rather than hidden: the semantic search drifts (querying "urban
public open space" returned PM2.5 variables, which is exactly why the crosswalk needs human
review), and the modelled-estimate flag is name-based and under-detects — `AIR_DEATH_R` is
modelled but does not say so in its name.

[Latest coverage report](https://sarapis.github.io/undatacommons-nyc/artifacts/coverage-latest) ·
regenerate with `python3 probe/coverage_probe.py`.
