---
layout: default
title: Decision log
---

# Decision log

Newest first. Record the *why*, not just the what — this is what makes a past choice reviewable.

## 2026-09-16 — Match against the 519 named indicators, not all 689

170 of the 689 base indicators carry no name in any source we hold: they return neither metadata
nor observations. The inverse crosswalk originally fell back to the DCID mnemonic, so a quarter of
"the framework" was represented by query strings like `DI ILL OUT`.

Nothing can match that. It inflated the tail — datasets looked further from the framework than they
were — and put mnemonics in the nearest-indicator column, where `VC VAW SXVLN` was reported as a
cluster's closest SDG concept. Excluding them moved every weak positive control up by 4–16
percentile points.

The count of what was excluded is printed on the page. An analysis that quietly matches against
garbage text and reports the resulting distance as a finding is measuring its own inputs.

## 2026-09-16 — Pool the non-English catalogs into one run, never one run per language

Cosine similarities from two different embedding models are not comparable, so the language groups
cannot be merged after the fact. But per-language runs would give five score spaces with two to
four cities each, and the evidence unit in this analysis is *how many independent cities* a theme
appears in — which two cities cannot support.

Pooled under the multilingual model they share one space and eleven cities. The cost is that the
weakest language sets the floor: Portuguese controls land at the 32nd and 44th percentile against
89th for Italian, so the Brazilian portion of the tail is the least trustworthy part of the run,
and the page says so.

## 2026-09-16 — A cluster carries its own coherence, or it is not a finding

k-means returns *k* clusters whether or not *k* themes exist in the data. The inverse crosswalk's
first run reported 24 of them as "themes"; reading the rows showed roughly half were mush — one
labelled "school" held building violations and lobbyist registrations.

Every cluster now carries the mean cosine of its members to its own centroid, and below 0.62 it is
published as **diffuse** rather than read as a theme. Cluster labels also require a term to cover a
fifth of the members, not merely to be distinctive: lift alone labelled a 144-member cluster
"inch, sea, rise" off a handful of coastal datasets.

The rule generalises past clustering: any method that always returns an answer has to be made to
report how much of an answer it actually found.

## 2026-09-16 — Evidence in the inverse crosswalk is counted in cities, never in datasets

A dataset far from every SDG indicator may be a gap in the framework, or may be a dataset the
matcher missed — and we cannot tell which from the dataset alone. A positive control proved it:
NYC's *Housing Maintenance Code Violations* is a hand-verified match for 11.1.1 and lands at the
24th percentile, inside the tail.

So a theme counts only through the number of **independent city catalogs** it appears in. One city
publishing forty parking files is a filing habit; twenty cities each publishing one is a category
of municipal governance. This is the same discipline as reporting a table across all cases rather
than testing one, applied to a corpus instead of a function.

## 2026-09-16 — An indicator is its own control group

The smell test's first sweep returned 41,350 findings — 5.4% of every observation in the graph,
which is a broken instrument rather than a result. 23,172 of them were negative percentages, and
nearly every one was correct: the `Percent` unit covers bounded proportions *and* signed growth
rates, balances and changes, with nothing in the unit string to separate them.

What separates them is frequency. A rule broken by most of an indicator's observations is its
definition; a rule broken by three country-years out of three thousand is an error. So checks are
suppressed per-indicator when they fire often enough to be structural, and the `outlier` check
compares each value against its own indicator's 99th percentile rather than against what a unit
is supposed to mean.

**Suppressions are published, not dropped.** The list of indicators that publish signed values
under a `Percent` unit is a finding about the graph's vocabulary, and a report that hid it would
look cleaner than the data is.

## 2026-09-16 — Gate checks on the shape of the data, never on a list of units

The first attempt to quiet the jump check whitelisted percent/count/rate units. It worked, and it
silently discarded Mauritius' food waste going 207 tonnes to 177,570 tonnes in one year, because
`WEIGHT_TN` was not on the list — precisely what the check exists to find. Unit vocabularies are
long, inconsistent and not ours to enumerate.

The durable test is a property of the values: does this indicator ever go negative anywhere? If
so it has no meaningful zero and no ratio on it means anything. That one question replaced the
whitelist and costs nothing to maintain.

## 2026-09-16 — The launch check is a diff against a recorded baseline, not a health check

A health check asks "does it answer?" and the platform would have passed one all week. The thing
that could break the demo is subtler: a DCID quietly withdrawn or redefined, which returns an
empty result — the same shape as a country that does not report. So `probe/launch_diff.py` records
a full snapshot (every crosswalk variable, every series value by value, every peer comparator, the
enumerated corpus, the tool list) and compares the next run against it field by field.

Two consequences worth keeping. **The baseline is only updated deliberately** (`--set-baseline`),
because a checker that re-baselines on every run reports "no change" forever. And **the diff has
its own self-test** (`--self-test`), which injects each drift class into a copy of the baseline and
asserts it is reported: a diff that returns "no change" and a diff that cannot see change look
identical from the outside.

## 2026-09-16 — Hardcode human-resolved DCIDs; never resolve by search at runtime

Between 14 and 16 Sep, with no code change on our side, `search_indicators` returned 44 candidate
variables for our fifteen topic queries and then 56 — nine topics gained, none lost, and every
row present on both dates identical in every field. The graph did not move; retrieval over it did.
Notably, "road traffic deaths" began returning `undata/sdg/SH_STA_TRAF`, the exact DCID our
road-deaths pair uses, which it had not on the 14th.

Discovery through search stays the rule (REST is federated and will answer for other publishers).
But once a human has resolved and graded a DCID it goes in `crosswalk.json` as a literal. A demo
that resolves by search at showtime can change its answer while the data stands still.

## 2026-09-14 — The human grade vetoes every mechanical check

The pair probe initially reported BLOCKED and CONTEXT pairs as chartable: resolution, unit and
overlap checks all passed, so it waved through pairs a human had judged incomparable. Now the
grade overrides, and a trend requires five overlapping years rather than a shared endpoint.

Kept as a decision because the pull to let the automated check "win" will recur every time
someone adds a pair. Units agreeing is necessary and nowhere near sufficient.

## 2026-09-14 — Missing denominator years stay empty

There is no ACS 1-year release for 2020, so NYC rates have no 2020 value — on the year homicides
spiked. Interpolating would produce a number visually identical to a measured one, in precisely
the case someone would quote it. The probe records dropped years explicitly.

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
