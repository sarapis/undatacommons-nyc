---
layout: default
title: "NYC's own Data Commons is running at commons.databook.nyc"
author: Devin Balkind
date: 2026-09-21 22:28:59 -0400
---

We have been arguing that a city should publish indicators rather than only tables. As of
today there is one to look at: **[commons.databook.nyc](https://commons.databook.nyc)**, a
custom Data Commons instance holding NYC's own series.

**11 variables, 410 observations**, every one read back out of the running instance over the API
and matched against the CSV that produced it. Nine are the crosswalk pairs whose NYC side was
already in observation shape — PM2.5, homicide, waste recycled, road deaths, child and maternal
mortality, air-pollution deaths, inadequate housing, municipal waste. Two more exist only to
answer a question we refused to reason about.

## The question that changed the pitch

Nobody had checked what the platform does below annual granularity. NYC's structural advantage
over a national graph is **frequency** — daily and monthly data the UN system does not hold — so
if that degraded on load, the case for this whole approach would have been weaker than we were
saying.

So it was tested rather than argued: DSNY's tonnage file is natively monthly and both waste
series already sum it to years, which means the *same rows* could be loaded twice, differing only
in the granularity of the date column. **260 month-granularity observations came back as months**,
rendered as months, with the seasonal cycle intact. The advantage survives.

## What it cost, and what it can carry

One Hetzner cpx32 — 4 vCPU, 8 GB, **€41.99/mo**. Memory is about half what the same containers
use under emulation on a Mac: 1.9 GB resident with NL search on, against 8.9 GB of images.

Capacity is a belief we tested lightly and will not overstate: 20 observation queries at 10-way
concurrency all answered, mean 1.4 s — and one page render returned 502 during that burst. **A
team's tool, not public-traffic infrastructure**, until somebody runs a real load test.

## Two findings worth more than the deployment

**The caveat is one click further away than the citation.** Each variable's comparability grade,
its reason, its tier and the UN series it maps to are carried in the MCF `description`, land in
the database, and are displayed in full on the knowledge-graph page. They are **absent** from the
chart's "About this data" dialog, which shows source and citation only. The thing this project
most wants attached to a number is the one thing the chart surface does not carry.

**A blank unit renders as `Count`.** On a per-100,000 rate that is not a missing label but an
incorrect one, which is worse than the blank it replaced. There is no unit in the base graph
meaning "per 100,000 people", so we defined `Per100kPeople` and `KgPerPerson` as `UnitOfMeasure`
instances in MCF. Establishing that took an experiment rather than a guess: **the timeline axis
renders a unit's DCID and ignores both `name` and `shortDisplayName`**, so a custom unit's DCID
*is* its display string. The first attempt produced the axis label
`Count (PerOneHundredThousandPeople)`.

## And the failure that names this project

The first load reported `status = SUCCESS`, `metadata = {'numVars': 0, 'numObs': 0}`, and exited
**0**. Every variable existed, the embeddings built, the site came up — against an empty database.
`INPUT_DIR` is flat, the loader globs it for `*.csv` and never resolves `config.json`'s file keys
as paths, and our CSVs were one directory down.

**The exit code is not the evidence; the row count is.** The runner now greps both numbers out of
the log and fails loudly on a zero, and `verify.py` reads every series back out of the instance
before a load is called done.

## Next

Council district, NTA, community district and police precinct **do not exist as classes in the
base graph at all** — city, borough, census tract, ZCTA, school district and state do. Publishing
NYC data by council district means defining the class and its entities in MCF, which is supported
work with a known shape rather than an open question.

The code lives in a separate workspace, `~/Antigravity/nyc-datacommons`, which is **local only
and has no remote yet** — so unlike this repo, the instance's build is not public.
