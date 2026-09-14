# UN Data Commons × NYC

Working repo for our UN System Data Commons hackathon project (Google NY, September 2026).

**Collaborators: paste this URL into Claude to get current on the project.**

```
https://sarapis.github.io/undatacommons-nyc/
```

That page is written for both people and AI assistants — it carries the current state of the
analysis, the verified platform findings, and links to every artifact we generate.

## What we are building

A **live Voluntary Local Review workbench**. NYC published the world's first VLR of the SDGs in
2018; it is a PDF produced every few years. NYC Open Data and the Mayor's Management Report
publish the same underlying indicators continuously, and the UN System Data Commons now holds
the authoritative global series. Nobody has connected the two for the person who needs it — the
analyst writing a budget justification or council testimony.

The hard part is not plumbing. **The UN graph is national-level: NYC resolves as a place but
carries zero UN observations.** So the crosswalk — with an explicit comparability grade on every
mapping — is the product, not a feature of it.

## Repo layout

| Path | What it is |
|---|---|
| `docs/` | The briefing hub, served at the URL above |
| `docs/_posts/` | Activity feed entries — one file per update |
| `docs/findings/` | What we verified against the live platform |
| `docs/artifacts/` | Generated outputs (coverage reports) |
| `probe/` | The coverage probe harness |

## Posting an update

```bash
./tools/new-update.sh "Short title here"
```

Creates `docs/_posts/YYYY-MM-DD-slug.md`. Write the body, commit, push. The briefing page is
current state and gets overwritten; the feed is history and never does — if a finding
invalidates the briefing, do both.

## Running the probe

No dependencies beyond a stock `python3`:

```bash
python3 probe/coverage_probe.py            # default candidate list
python3 probe/coverage_probe.py --peers    # also probe peer countries
```

Writes a graded report to `docs/artifacts/`. See [probe/README.md](probe/README.md).
