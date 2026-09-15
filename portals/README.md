# City open data portal inventory

Surveyed 2026-09-15.

> **Correction.** This file previously claimed no global registry of CKAN portals exists. That was
> wrong. The **[CKAN Ecosystem Catalog](https://ecosystem.ckan.org)** — a 2025 NSF POSE II project
> from the CKAN core team, WPRDC and datHere — lists **199 instances, 97 of them local or regional
> government**, with machine-readable data at
> [`ckan/ckan-instances`](https://github.com/ckan/ckan-instances). We found only its dead
> predecessors because we searched for the registries we already knew about. It is now the primary
> CKAN source here; the site itself sits behind Cloudflare, so fetch the GitHub repo.

The older registries have genuinely rotted, which is what misled us:

| Source | Status |
|---|---|
| `ckan.org/about/instances` | 404 |
| `dataportals.org` API | 404 (site alive, API gone) |
| `opendatainception.io` | serves a broken payload |
| Socrata `/api/catalog/v1/domains` | 404 — retired |
| `catalog.data.gov` CKAN API | 404 |
| `data.gov.uk` CKAN API | 403 |
| OKFN `dataportals.org` CSV on GitHub | **alive**, 631 rows, barely maintained |

So an inventory has to be *constructed and re-verified*, not looked up.

## What is here

- **`socrata-domains.json`** — 159 live Socrata domains with the dataset count seen per domain.
  Harvested by paging the Discovery catalog and collecting `metadata.domain`, then widened with a
  100-category sweep. **A floor, not a census:** the catalog caps `resultSetSize` at 10,000 and a
  flat page-through is dominated by publishers with thousands of datasets, so small municipal
  portals surface only via the category slices.
- **`ckan-live.json`** — 39 CKAN instances confirmed live by fingerprinting each OKFN candidate
  with `/api/3/action/status_show`, which returns the CKAN version when a site is CKAN and is not
  blocking. Includes Boston, San José, Madrid, Milan, Matera, Buenos Aires, Alberta,
  opendata.swiss.

## Reproducing

```bash
python3 portals/harvest_socrata.py   # -> socrata-domains.json
python3 portals/probe_ckan.py        # -> ckan-live.json   (needs portals.csv from OKFN)
```

## The finding worth carrying

**39 of 631 OKFN candidates answer — about 6%.** That measures link rot in an abandoned registry,
not CKAN's popularity, and it is why the maintained CKAN Ecosystem Catalog matters.

And "does not answer" is not "is dead". Of the official catalog's 174 additional entries only ~50
answer an anonymous `package_search`, but `data.gov`, `govdata.de` and `data.overheid.nl` are
plainly alive and simply refuse the probe. The count measures *what responds to this specific
anonymous API call*, and the inventory says so rather than calling the rest dead.
