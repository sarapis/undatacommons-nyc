---
layout: default
title: Decision log
---

# Decision log

Newest first. Record the *why*, not just the what — this is what makes a past choice reviewable.

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

## Open — peer-comparator framing

Compare NYC to peer *cities* (needs a non-UN source: OECD metro, Eurostat Urban Audit,
UN-Habitat) or to *nations* (free, honest, works today: "NYC's rate sits between Portugal and
Slovenia")? Blocks the benchmark view design. **Owner: Devin.**
