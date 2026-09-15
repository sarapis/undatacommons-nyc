# City open data portal inventory

Surveyed 2026-09-15. **There is no global registry of open data portals.** Every canonical one
has rotted:

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

**39 of 631 OKFN candidates are live CKAN — about 6%.** That is not a statement about CKAN's
popularity; it is a statement about link rot in the only surviving registry. Any project that
assumes a maintained list of city portals exists is building on sand.
