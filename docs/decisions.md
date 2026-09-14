---
layout: default
title: Decision log
---

# Decision log

Newest first. Record the *why*, not just the what — this is what makes a past choice reviewable.

## 2026-09-14 — Comparators are tiered; city-level is the exception, not the rule

`URBANIZATION--DOU_CITY` gives a genuine NYC-vs-national-city-aggregate comparison across many
countries, but only for **five indicators** — it clusters in gridded-geospatial families and the
administrative indicators have no spatial dimension. Tier 1 (city aggregates, ~5 indicators),
Tier 2 (urban/rural, ~8, low NYC relevance), Tier 3 (national totals, everything else).

**Plan against Tier 3 as the default.** An earlier version of this entry recommended city
aggregates as the primary framing, generalising from PM2.5 alone; corrected the same day.

Caveat to carry onto any Tier 1 chart: NYC sits inside the US city aggregate, roughly 7% of it.

## 2026-09-14 — The pair probe does not assign comparability grades

The probe verifies that a mapping still resolves and that units agree. The grade itself stays a
human judgment recorded in `crosswalk.json`. A machine that scores comparability would be
confidently wrong exactly where it matters — the waste pair has agreeing units and is still not
an apples-to-apples comparison, because NYC counts residential collection and the UN counts all
municipal waste.

## 2026-09-14 — Road safety is out as the headline demo indicator

SDG 3.6.1 returns one observation for the US (2021). Our application used road safety as the
worked example. Replacing it with a GREEN-graded indicator from the coverage report; homicide
rate and municipal waste recycling are the strongest candidates because NYC publishes closely
matching series.

## 2026-09-14 — Collaboration hub is a fetchable site, not an MCP server

A URL works in every Claude surface with zero setup for collaborators. An MCP connector is
richer but each person has to configure it, and it is only available on some surfaces. The site
is a prerequisite for the MCP option anyway, so this is sequencing rather than exclusion.

## 2026-09-14 — Probe harness is stdlib-only Python

Three people on different machines need to run it without a virtualenv debugging session.
`certifi` is used when importable and falls back to the system trust store.

## Superseded — peer-comparator framing

Was: compare NYC to peer *cities* (needs a non-UN source) or to *nations*? The DOU_CITY finding
above gives a third and better answer. Kept for the record.
