# UN Data Commons × NYC — agent context

Hackathon project: a live Voluntary Local Review workbench bridging NYC Open Data and the
UN System Data Commons.

**Read `docs/index.md` first.** It is the project briefing and is kept current.

## Hard-won rules — do not relearn these the expensive way

- **The UN graph is national-level.** NYC resolves as `geoId/3651000` but has zero UN
  observations. Any design that assumes you can look NYC up in the UN graph is wrong.
- **Discover variables through MCP, never through REST.** The MCP surface only returns governed
  `undata/` variables. REST is federated with the wider Data Commons graph and will answer for
  other publishers without warning.
- **Never guess a DCID.** The server's own instructions forbid it and a guessed DCID returns an
  empty result rather than an error, which is worse. Resolve via `search_indicators`.
- **Check coverage before designing around an indicator.** Run `probe/coverage_probe.py`.
  Series density varies from 1 observation to 300+.
- **Every datapoint keeps its attribution.** The platform requires it and our QA approach
  promises it.

## Layout

- `docs/` — the briefing hub, served at https://sarapis.github.io/undatacommons-nyc/
- `docs/artifacts/` — generated outputs; regenerate rather than hand-edit
- `probe/` — the coverage probe harness (stdlib only)

## Conventions

- Record choices in `docs/decisions.md` with the reasoning, newest first.
- Update the `Last updated` date in `docs/index.md` when you change it.
