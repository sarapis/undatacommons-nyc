---
layout: default
title: Decision log
---

# Decision log

Newest first. Record the *why*, not just the what — this is what makes a past choice reviewable.

## 2026-09-14 — Recommend national city aggregates as the peer comparator

`URBANIZATION--DOU_CITY` turns out to exist for many countries with full 10-year series, so NYC
can be compared to the city aggregate of the UK, France, Japan, Mexico and others from UN Data
Commons alone. One source, one method, one unit, no cherry-picked comparator city. Supersedes
the open question below. **Recommended, not yet confirmed — Devin's call.**

Caveat to carry onto any chart: NYC sits inside the US city aggregate, roughly 7% of it.

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
