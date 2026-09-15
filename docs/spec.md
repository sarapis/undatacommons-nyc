---
layout: default
nav_id: spec
title: Comparability Spec
---

# City ↔ UN Comparability Spec

**Version 0.1 · draft for comment · 2026-09-15**

A vocabulary for recording *whether two statistics may be compared, and what the comparison is
worth.* Written for cities producing Voluntary Local Reviews against the UN System Data Commons,
and for the tools they build.

> **The problem this addresses.** Joining a city indicator to a UN indicator is easy. Knowing
> whether the join is legitimate is the hard part, and it is currently done privately,
> inconsistently, and usually in a footnote nobody reads. More than 200 cities now produce VLRs.
> Every one of them is making these judgments; almost none of them are recording them in a form
> another city, or a tool, can use.

This spec is deliberately small. It is a vocabulary and five rules, not a methodology.

---

## 1. Grades

Every mapping between a local series and a UN series **MUST** carry exactly one grade.

| Grade | Definition | You MAY |
|---|---|---|
| **DIRECT** | Same concept, same population, same unit and denominator, comparable collection method. | Chart on one axis without qualification. |
| **PROXY** | Same concept, comparable in level, with a documented methodological difference (e.g. modelled estimate vs administrative count). | Chart on one axis, with the difference stated on the chart. |
| **CONTEXT** | Related but not equivalent — different age band, denominator, measure type, or underlying concept. | Show side by side, clearly labelled as different measures. **MUST NOT** share an axis. |
| **RANK-ONLY** | The comparator exists for a single period. A cross-sectional placement is possible; a trend is not. | Report a rank for that period. **MUST NOT** present as a trend. |
| **BLOCKED** | A comparison cannot presently be made. The blocker **MUST** be named. | Nothing, until the named blocker is resolved. |
| **NO-SOURCE** | No local counterpart has been identified. | Nothing. Record it so the gap stays visible. |
| **NO-SIGNAL** | Both sides are flat or at a ceiling; the comparison carries no information. | Nothing. Record the judgment so it is not rediscovered. |

A grade is a **human judgment**. It is not derived from the data, and tools **MUST NOT** compute
or override it.

## 2. Tiers

A grade says whether a comparison is legitimate. A tier says **what it is worth**. Every mapping
**MUST** carry one.

| Tier | Comparator | Note |
|---|---|---|
| **1** | The city against other countries' **city aggregates** | Like-for-like. Rare — it requires the publisher to disaggregate by settlement type. |
| **2** | Against **urban aggregates** | Bundles cities with towns and suburbs. Coarser than it looks. |
| **3** | Against **whole nations** | Real context, not a peer comparison. Cities typically diverge from their national averages, often sharply. |

Tier 3 is the common case and **MUST** be labelled as such wherever a figure is presented. A city
is not a country, and a reader who is not told will assume otherwise.

## 3. Required provenance

Every value presented under this spec **MUST** carry:

- **source** — the publishing organisation and dataset or variable identifier
- **vintage** — the observation period, and the retrieval date where the source is revisable
- **unit** — including the denominator where the figure is a rate
- **method class** — at minimum whether the figure is an *administrative count*, a *survey
  estimate*, or a **modelled estimate**

The method class is not optional. A modelled estimate beside an administrative count is the single
most common way a defensible-looking chart misleads.

## 4. The five rules

**R1 — The human grade vetoes every mechanical check.**
Resolution, unit agreement and period overlap are necessary conditions. None of them, in any
combination, establishes comparability. Where an automated check and a recorded grade disagree,
the grade wins.

**R2 — Agreeing units are necessary and never sufficient.**
Two raw counts share a unit. So do a count of deaths under five and a count of deaths under one.

**R3 — Missing data stays missing.**
A gap **MUST NOT** be interpolated, and a derived rate **MUST NOT** be published for a period
whose denominator is estimated rather than measured. An invented value is visually
indistinguishable from a measured one, and will be quoted as though it were.

**R4 — Record why a mapping fails, not merely that it did.**
The reason is the durable artifact. A list of failures without reasons will be re-derived by the
next person, and re-derived differently.

**R5 — Ambiguity resolves to candidates, never to a guess.**
Where a query matches more than one mapping, a conforming tool **MUST** return the candidates and
**MUST NOT** silently select among them.

## 5. Record format

A conforming crosswalk is a JSON document. Schema:
[`spec/comparability-v0.1.schema.json`](https://github.com/sarapis/undatacommons-nyc/blob/main/spec/comparability-v0.1.schema.json).

```json
{
  "id": "child-mortality",
  "grade": "CONTEXT",
  "tier": 3,
  "reason": "AGE BANDS DO NOT MATCH. The UN counts deaths under five; the local series counts deaths under one. Both are raw counts, so the units agree — which is the trap.",
  "comparator": {
    "source": "undata/who/CHILD_DEATHS.AGE--Y0T4",
    "place": "country/USA",
    "method_class": "modelled_estimate"
  },
  "local": {
    "source": "fcau-jc6k",
    "method_class": "administrative_count"
  }
}
```

`reason` is **REQUIRED** for every grade other than DIRECT, and **SHOULD** name the specific
difference rather than restating the grade.

## 6. Conformance

An implementation conforms if it:

1. carries exactly one grade and one tier per mapping;
2. supplies a `reason` for every non-DIRECT grade;
3. presents no figure without source, vintage, unit and method class;
4. refuses to place CONTEXT, BLOCKED, NO-SOURCE or NO-SIGNAL mappings on a shared axis;
5. lets a recorded grade override any automated check (R1);
6. interpolates nothing (R3);
7. returns candidates on ambiguity (R5).

## 7. Reference implementation

This spec is a description of working software, not a proposal.

- **Crosswalk** — [`probe/crosswalk.json`](https://github.com/sarapis/undatacommons-nyc/blob/main/probe/crosswalk.json), 12 mapped pairs
- **Validator** — `python3 probe/validate_crosswalk.py`, which checks the crosswalk against the schema and the conformance rules
- **Agent interface** — [`mcp/server.py`](https://github.com/sarapis/undatacommons-nyc/tree/main/mcp), an MCP server that refuses on non-chartable grades and returns the reason
- **Worked output** — [the demo](https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html)

## 8. Status and what would improve it

Version 0.1, drafted from one city's crosswalk against one publisher. Its obvious weaknesses:

- The grades were derived from **12 mappings in a single city**. A second city will find cases
  they do not cover.
- **`method_class` is coarse.** Three values is probably too few; survey methodology varies more
  than that.
- **Tiers are specific to the degree-of-urbanisation taxonomy** the UN uses. A publisher that
  disaggregates differently would need a fourth tier or a different axis.
- Nothing here addresses **sub-city** comparison, which is what most city analysts actually want.

Corrections and counter-examples are more useful than adoption at this stage.
[Open an issue](https://github.com/sarapis/undatacommons-nyc/issues).
