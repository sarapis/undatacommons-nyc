# Coverage probe

Finds out which UN indicators can actually carry a chart, before we design around them.

## Why this exists

SDG 3.6.1 (road traffic deaths) looks like the perfect demo indicator for a city audience.
Against the live platform it returns **exactly one observation** for the United States, in 2021.
You cannot draw a trend through one point. Meanwhile UNICEF's population series returns 26
annual points, so the sparsity is real rather than an API quirk.

Choosing indicators by intuition is how you end up on stage with a one-point chart. This sweeps
a candidate list and grades every variable on evidence.

## Usage

```bash
python3 probe/coverage_probe.py             # default candidate list
python3 probe/coverage_probe.py --peers     # also probe peer countries
python3 probe/coverage_probe.py --limit 12  # more results per topic
```

Stdlib only — no virtualenv needed. If TLS verification fails on macOS, `pip3 install certifi`.

Edit `candidates.json` to add topics. The probe is cheap; add freely.

## Grades

| Grade | Meaning |
|---|---|
| **GREEN** | ≥5 observations over ≥5 years, latest point 2018 or newer — chartable |
| **AMBER** | Sparse. Usable as a single level with a caveat, not as a trend |
| **RED** | One point or none. Cannot support the chart we had in mind |

A RED row is not a broken query. It is the platform telling us something true.

## Flags

- `modelled_estimate` — the UN figure is a modelled estimate, not an administrative count.
  Pairing one with a NYC incident count needs an explicit caveat on the chart. The heuristic
  is name-based and **under-detects**: `AIR_DEATH_R` is modelled but does not say so in its
  name. Treat it as a prompt for human review, not as ground truth.
- `governed` — the DCID sits inside the `undata/` namespace. The MCP surface only returns
  governed variables; REST is federated with the wider Data Commons graph and will answer for
  other publishers without warning. Discover through MCP, always.
