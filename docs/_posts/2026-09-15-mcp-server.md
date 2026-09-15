---
layout: default
title: "The MCP server that refuses"
author: Devin
date: 2026-09-15 20:00:00 -0400
---

The application promised three layers: a crosswalk, benchmark views, and an agent. Two were
built. This is the third.

`mcp/server.py` composes the UN System Data Commons with NYC Open Data and serves the graded
crosswalk over MCP. Stdlib only, no framework, no virtualenv:

```bash
claude mcp add nyc-un-benchmarks -- python3 /path/to/undatacommons-nyc/mcp/server.py
```

## The point is that it refuses

Every other agent tool in that room will answer. This one returns a comparison only where a human
graded the pair DIRECT or PROXY. For CONTEXT, BLOCKED and RANK-ONLY it declines and names the
definitional difference:

```
benchmark("child mortality")
  → refused: true, grade: CONTEXT
    "AGE BANDS DO NOT MATCH. The UN counts deaths under five; NYC's series counts
     deaths under one. Both are raw counts so the units agree — which is the trap."
    what_is_possible: "Show the two series side by side, never on one axis."
```

The refusal carries `guidance: "This is a refusal, not an error. Report the reason to the user;
do not route around it by fetching the sides separately."` — because an agent's instinct on being
blocked is to find another way, and here the block *is* the answer.

That makes a **trust & QA gate a tool contract** rather than a policy document. It is the
afternoon's topic arriving as working software.

## Three behaviours worth stealing

**Ambiguous names return candidates, not a guess.** "municipal waste" matches two mapped
indicators. The server says so and asks you to choose. Silently picking one is exactly the quiet
guess this project exists not to make.

**A missing comparator is reported as a finding.** `benchmark("municipal-waste")` refuses because
the UN holds *zero* US observations — and points at `world_position`, since 90 other countries do
report it. Not a gap in the tool; the declared comparator reports nothing.

**Derivations are data the server executes, not prose it ignores.** The municipal-waste pair
declares its short-ton assumption and per-capita conversion in `crosswalk.json`, and the server
runs it. The demo and the server now produce identical figures — 397.9 kg per capita, 41st of 91 —
which is the check that they have not drifted.

## Four bugs found by building it

The server is an interface over work we had already verified, and it still surfaced four errors:

- The crosswalk had **11 pairs, not 12**. Municipal waste existed only in the demo; the briefing
  already claimed 12. Now in `crosswalk.json`, which is the source of truth.
- `benchmark("road deaths")` matched nothing — "road deaths" is a substring of neither
  `road-deaths` nor "Road traffic deaths". Now matched on word overlap.
- The municipal-waste SoQL returned **nothing at all**: `sum(a + b + c)` is NULL whenever any
  column is NULL, and several DSNY streams did not exist in early years. Fixed with `coalesce`.
- Per-capita derivation existed only in the demo script, so the server would have served raw tons
  against country tonnes. Implemented properly rather than left as prose.

`python3 mcp/smoke.py` now checks every tool and asserts the figures against the demo's published
numbers. 8/8.
