---
layout: default
title: "The UN graph is national-level — NYC has no UN data"
author: Devin
date: 2026-09-14 09:00:00 -0400
---

Probed the live staging deployment before writing any integration code. The headline result
changes the shape of the project.

NYC **resolves** as an entity in the graph (`geoId/3651000`, type `City`) but appears in *no*
variable's `placesWithData` — not for road deaths, not for PM2.5, not even for total population.
Scoping a search to NYC alone returns zero variables and zero topics. `places` turns out to be a
hard availability filter, not a hint.

So there is no "look up NYC in UN Data Commons," and anything that assumed we would query both
sides and join is wrong. **The crosswalk is the product, not a feature of it.** That is
awkward for the build but good for the pitch — the gap we proposed to fill is verifiably there.

Two supporting findings. The MCP surface only ever returned governed `undata/` variables, while
REST is federated with the wider Data Commons graph and will answer for other publishers without
warning — so discovery goes through MCP, always. And provenance is first-class: every
observation carries a `provenanceUrl`, an `observationPeriod`, and a unit DCID that encodes the
denominator, which means part of our comparability check can be automatic rather than
hand-curated.

Full detail and reproducible commands:
[platform probe findings](https://sarapis.github.io/undatacommons-nyc/findings/2026-09-14-platform-probe).
