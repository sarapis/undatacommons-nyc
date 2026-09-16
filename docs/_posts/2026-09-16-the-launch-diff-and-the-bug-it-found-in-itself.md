---
layout: default
title: "The launch diff, and the bug it found in itself"
author: Devin Balkind
date: 2026-09-16 11:05:00 -0400
---

The platform goes fully public tomorrow, 17 Sep. Every figure this project publishes was measured
against the pre-launch deployment, and the open question in the briefing was blunt: *will staging
DCIDs survive the launch?* A withdrawn DCID does not raise an error. It returns an empty result,
which is the same shape as a country that does not report — so the demo would show a blank chart
to a room at Google NY and nothing would look broken until someone asked.

So: re-ran every probe against the live deployment and diffed it against 14 Sep, and built
`probe/launch_diff.py` so that tomorrow's version of this is one command rather than an afternoon.

## The graph has not moved

| What | 14 Sep | 16 Sep |
|---|---:|---:|
| SDG base indicators enumerated | 689 | **689** |
| Variant DCIDs beneath them | 6,025 | **6,025** |
| Indicators screened, every field compared | 689 | **689, zero changed** |
| Crosswalk series (variable × place), value by value | — | **57 checked, zero changed** |
| Crosswalk variables, via metadata | — | **12 checked, zero changed** |
| Demo figures (`mcp/smoke.py`) | 8/8 | **8/8** |

Not one DCID added, not one removed, not one value revised, not one unit changed. The three
`EMPTY` series are the ones we already knew about — the UN holds no municipal-waste observations
for the US, Japan or Mexico, which is the finding the municipal-waste card is built on.

The only differences anywhere in the crosswalk were ours, not the platform's: two figures in NYC's
housing dataset moved by one (297,753 → 297,754 — NYC Open Data is live), the road-deaths pair
was regraded BLOCKED → RANK-ONLY by hand yesterday, and the municipal-waste pair is new since the
14th.

## The search surface *has* moved

The coverage probe grades whatever `search_indicators` returns for fifteen topic queries. Same
code, same queries, same host, two days apart:

- **44 candidate variables → 56.** Nine of fifteen topics gained rows. **None lost any.**
- Every row present on both dates is **identical in all fifteen fields**.
- So the grade mix moved — 30 GREEN / 9 AMBER / 5 RED → **36 / 11 / 9** — entirely because search
  returned more to grade, not because anything got better or worse.

The one worth noting: searching "road traffic deaths" on 16 Sep returns
`undata/sdg/SH_STA_TRAF` — the exact DCID our road-deaths pair uses — and on the 14th it did not.
Recall improved. That is good news and a warning in the same breath: **the graph is frozen, the
retrieval over it is not.** Anything that resolves a DCID by searching at runtime can change its
answer without the data changing at all. Our crosswalk hardcodes DCIDs that a human resolved once,
which is exactly why the demo is insulated from this. It was a chore to do it that way. It is not
a chore any more.

I checked the obvious alternative explanation before writing this down: `search_indicators`
returns byte-identical results across three consecutive calls today, and neither
`coverage_probe.py` nor `candidates.json` has been touched since the initial commit.

## The bug it found in itself

The first run of `launch_diff.py` reported, confidently, that **all twelve crosswalk DCIDs were
missing from the graph** — while `get_observations` was returning data for every one of them.

`get_variable_metadata` requires `entity_dcids`. Omit it and the server answers **200 with a
completely empty body** — no error, no `status` field, no `variables` key at all. A caller that
trusts the response shape reads that as "every variable has been withdrawn". Two days before the
launch it was written to detect, the launch detector was ready to cry wolf about the entire
crosswalk.

That is the seventh entry in this project's list, and it was caught the same way as four of the
other six: by printing a table of all twelve rows and reading it, rather than trusting a summary
count. A checker that reports catastrophe is at least loud. The version of this bug that would
have actually hurt is the mirror image — a diff that stays quiet because it cannot see.

So `launch_diff.py --self-test` now injects each drift class into a copy of the baseline and
asserts the diff reports it: a revised value, a series going empty, a series coming back, a
changed unit, a shortened span, a renamed variable, a withdrawn variable, an indicator dropping
out of the corpus, a tool disappearing from the server. Plus the converse — an unmutated copy must
report nothing. **10/10.** A diff that returns "no change" and a diff that cannot see change are
indistinguishable from the outside, and this project has shipped that mistake often enough to stop
paying for it twice.

## Tomorrow

The baseline is recorded as of today, pre-launch. After the platform goes public:

```bash
python3 probe/launch_diff.py        # exits non-zero if anything moved
python3 mcp/smoke.py                # the demo's published figures
```

If the public deployment answers on a different host, `UNDC_ENDPOINT` and `UNDC_REST` override it
without a code edit, and the diff reports the host change as drift in its own right. As of this
afternoon no public hostname resolves yet — `undatacommons.unicc.biz` and `datacommons.un.org`
both refuse to connect, and the deployment we have been building against is still answering
normally.
