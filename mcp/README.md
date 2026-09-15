# NYC ↔ UN benchmark MCP server

Serves the hand-graded crosswalk over MCP, so an agent can ask for a benchmark in one call
instead of reading a website.

**The point of this server is that it refuses.** Most tooling answers. This returns a comparison
only where a human graded the pair DIRECT or PROXY; for CONTEXT, BLOCKED and RANK-ONLY it declines
and names the definitional difference that stopped it.

```
benchmark("child mortality")
  → refused: true, grade: CONTEXT
    "AGE BANDS DO NOT MATCH. The UN counts deaths under five; NYC's series counts
     deaths under one. Both are raw counts so the units agree — which is the trap."
```

The failure mode this guards against is not a missing number. It is a plausible chart built on
two things that were never the same measurement.

## Run it

Stdlib only — no framework, no virtualenv:

```bash
python3 mcp/server.py
```

Then point an MCP client at that command. For Claude Code:

```bash
claude mcp add nyc-un-benchmarks -- python3 /absolute/path/to/undatacommons-nyc/mcp/server.py
```

A `CENSUS_API_KEY` in the environment or in `.env` is needed for rate-based indicators (NYC
publishes counts, the UN publishes rates per 100,000). Free key:
<https://api.census.gov/data/key_signup.html>.

## Tools

| Tool | What it does |
|---|---|
| `list_benchmarks` | Every mapped pair with its grade and tier. Call this first. |
| `benchmark` | A comparison for one indicator and year — **or a refusal with the reason** |
| `world_position` | NYC's rank among every reporting country, with nearest neighbours |
| `explain_grade` | The definitional difference, denominator problem or coverage gap behind a grade |

It also serves `skill://nyc-benchmark-researcher/SKILL.md`, mirroring the UN Data Commons
server's own convention of shipping a playbook alongside its tools.

## What it composes

- **UN System Data Commons** via `probe/undc.py` — the governed `undata/` namespace only
- **NYC Open Data** via `probe/nyc.py` — the SoQL declared per pair in `probe/crosswalk.json`
- **Census ACS** via `probe/census.py` — denominators, since NYC publishes counts

Grades and reasons are human judgments read from `crosswalk.json`. The server executes the
crosswalk; it does not second-guess it.

## Behaviours worth knowing

- **Ambiguous names return candidates, not a guess.** "municipal waste" matches two indicators;
  the server says so and asks you to pick rather than choosing silently.
- **A missing comparator is reported as a finding.** `benchmark("municipal-waste")` refuses
  because the UN holds *zero* US observations for it — and points at `world_position`, since 90
  other countries do report it.
- **Derivations are declared as data and executed.** The municipal-waste pair converts both sides
  to kg per capita, including the short-ton assumption, rather than describing it in prose.
- **Years without a denominator are absent, never interpolated.** There is no ACS 1-year release
  for 2020, so 2020 carries no rate.

## Verifying

```bash
python3 mcp/smoke.py
```

Exercises every tool and checks the figures against the demo's published numbers.
