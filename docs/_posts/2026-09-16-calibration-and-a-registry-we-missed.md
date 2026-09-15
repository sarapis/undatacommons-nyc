---
layout: default
title: "Threshold calibration, and a registry we said didn't exist"
author: Devin
date: 2026-09-16 09:00:00 -0400
---

Two corrections and one fix. The corrections are the useful part.

## The CKAN registry exists. We said it didn't.

We reported that no global registry of CKAN portals survives — that every canonical one had
rotted. That was **wrong**.

The **[CKAN Ecosystem Catalog](https://ecosystem.ckan.org)** is a 2025 NSF POSE II project from
the CKAN core team, WPRDC and datHere. It lists **199 instances, 97 of them local or regional
government**, machine-readable at
[`ckan/ckan-instances`](https://github.com/ckan/ckan-instances).

We missed it because we searched for the registries we already knew about — `ckan.org/instances`,
dataportals.org, opendatainception — found all three dead, and concluded the category was dead.
The correct inference was that we were looking at the *previous generation*. (The site sits behind
Cloudflare and refuses both curl and a headless browser; the GitHub repo is the way in.)

The abandoned OKFN list really has rotted — 39 of 631 answer — which is what made the wrong
conclusion feel supported.

**Inventory now: 372 portals surveyed, 70 municipal, 543,000 datasets.**

And a related correction: a portal that does not answer an anonymous `package_search` is **not**
dead. `data.gov`, `govdata.de` and `data.overheid.nl` all refuse the probe and are plainly alive.
The inventory now reports what responds to one specific API call, which is a much weaker claim
than liveness.

## The threshold fix, and the wrong turn before it

An absolute similarity cutoff cannot travel between catalogs. Measured on hand-judged matches,
good pairs span **0.42–0.70 in NYC, 0.50–0.55 in Chicago, 0.37–0.59 in Madrid**. One number is
simultaneously too strict and too loose.

**The first fix was wrong, and instructively so.** We calibrated a z-score — how many standard
deviations the top match sits above the catalog's own distribution — measured F1 0.68 against a
labelled set, wired it in, and it admitted **60 of 80 indicators**. Two independent errors:

1. **The labelled set was biased.** Every case in it came from candidates that had *already
   passed* the old 0.50 filter, so we measured on a pre-selected population and learned nothing
   about what the filter should have rejected.
2. **z measures the wrong thing.** Against a catalog whose similarities cluster near zero, the top
   hit sits many standard deviations above the mean whether it is right or garbage. z describes
   how *peaked* a distribution is, not how good its winner is.

What actually varies between catalogs — and is the right thing to normalise — is the distribution
of **top-1 scores across all probed indicators**. The cutoff is now the best 20% of that, with an
absolute floor so a uniformly hopeless catalog cannot contribute its least-bad rows anyway.

| City | Cutoff | Candidates |
|---|---:|---:|
| Milan | 0.450 | 12 |
| Boston | 0.457 | 16 |
| Chicago | 0.473 | 16 |
| Madrid | 0.515 | 16 |

Bounded worksheets that adapt to each catalog, instead of 0 or 69.

## What has not changed

**No substantive SDG indicator has matched outside NYC.** Better calibration produces a better
worksheet; it has not produced a good mapping. NYC's pairs were found by a person who knew the
data, with the matcher confirming them, and nothing yet shows the matcher can lead.

That is worth saying plainly a week out from Builders' Day: the infrastructure generalises, the
judgment does not, and the judgment is the part that matters.
