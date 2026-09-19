#!/usr/bin/env python3
"""Country names, read off the platform and cached -- because one call does not name them all.

`get_child_observations(variable, Earth, Country)` returns an `entityMetadata` block that
names each child place. It names about 155 of them. Past that point the name is an empty
string, and the places dropped are always the alphabetical tail by DCID -- measured 19 Sep:

    VC_IHR_PSRC             198 entities, 154 named, first unnamed country/SHN
    EN_ATM_PM25 (DOU_CITY)  185 entities, 158 named, first unnamed country/SVK
    unicef/DM_POP           232 entities, 152 named, first unnamed country/NIC

Nothing in the response says a name was dropped, so a client that reads names off one call
labels South Africa, Sweden, the United States and forty others with nothing, and a fallback
to the DCID puts "country/USA" on a chart. `mcp/server.py` did exactly that in
`world_position`'s neighbours, and 563 of the 3,844 rows in the 18 Sep smell test carry no
`place_name` for the same reason. The 14 Sep post said "two countries return empty names".
Two was the number visible on one card, not the number the platform drops.

The fix is measured, not typed. A variable with fewer than ~150 reporting countries names
every one of them, so the tail is recoverable from the platform itself by taking the union
of names across calls. This script does that, records the cap it observed on every call,
and writes the union to probe/cache/country_names.json. `names_for(response)` is the one
function the server and the smell test call: the live names from a response, filled from
the cache, never a DCID.

Usage:
    python3 probe/country_names.py            # build or refresh the cache, print the table
    python3 probe/country_names.py --check    # measure the cap per call, write nothing
    python3 probe/country_names.py --budget 80

Stdlib only. Writes probe/cache/country_names.json and docs/artifacts/country-names-<date>.{json,md}.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "probe"))

from undc import Client, UNDCError  # noqa: E402

CACHE = ROOT / "probe" / "cache" / "country_names.json"
ARTIFACTS = ROOT / "docs" / "artifacts"

# The variables the demo, the server and the pair probe actually call, first. If the cap
# bites anywhere it bites here, and the coverage table should say so on these rows.
_SEEDS = ["undata/unicef/DM_POP"]


def _crosswalk_dcids():
    cw = json.loads((ROOT / "probe" / "crosswalk.json").read_text(encoding="utf-8"))
    out = []
    for p in cw["pairs"]:
        d = (p.get("un") or {}).get("dcid")
        if d and d not in out:
            out.append(d)
    return out


def _screened_dcids():
    """Usable indicators, sorted, so the walk is reproducible run to run."""
    s = json.loads((ROOT / "probe" / "cache" / "screened.json").read_text(encoding="utf-8"))
    return sorted(x["dcid"] for x in s["indicators"]
                  if x.get("grade") in ("GREEN", "AMBER", "RANK-ONLY"))


def load():
    """dcid -> name from the cache; empty if the cache has not been built."""
    if not CACHE.exists():
        return {}
    return json.loads(CACHE.read_text(encoding="utf-8")).get("names", {})


def names_for(response, cache=None):
    """Names for every place in a get_child_observations response.

    Live names win where the platform sent one; the cache fills the tail it dropped. A
    place named by neither is left OUT of the dict, so a caller that wants a label falls
    back deliberately (to the ISO code, say) rather than to whatever `.get` returns.
    """
    cache = load() if cache is None else cache
    out = {}
    places = set()
    for row in ((response.get("data") or {}).get("rows") or []):
        places.add(row[0])
    for row in ((response.get("entityMetadata") or {}).get("rows") or []):
        places.add(row[0])
        if row[1]:
            out[row[0]] = row[1]
    for p in places:
        if p not in out and cache.get(p):
            out[p] = cache[p]
    return out


def label(dcid, names):
    """A printable label: the name, else the ISO code -- never the bare DCID."""
    return names.get(dcid) or dcid.rsplit("/", 1)[-1]


def measure(response):
    """What one response reveals about the cap: entities, named, and where the tail starts."""
    rows = (response.get("entityMetadata") or {}).get("rows") or []
    named = sorted(r[0] for r in rows if r[1])
    unnamed = sorted(r[0] for r in rows if not r[1])
    first = unnamed[0] if unnamed else None
    # "clean tail" = every unnamed place sorts after every named one. If this is ever
    # False the cap is not alphabetical and the docstring above is wrong.
    clean = (not unnamed) or (not named) or named[-1] < first
    return {"entities": len(rows), "named": len(named), "unnamed": len(unnamed),
            "first_unnamed": first, "alphabetical_tail": clean}


def build(client, budget, check_only=False, quiet=False):
    names = {}
    seen = set()
    calls = []
    queue = _crosswalk_dcids() + _SEEDS + _screened_dcids()
    for dcid in queue:
        if len(calls) >= budget:
            break
        unnamed_seen = [p for p in seen if p not in names]
        # Stop early once every place we have ever seen carries a name -- but only after
        # the seeds, which are the calls the coverage table exists to report on.
        if len(calls) >= len(_crosswalk_dcids()) + len(_SEEDS) and seen and not unnamed_seen:
            break
        try:
            r = client.call_tool("get_child_observations",
                                 {"variable_dcid": dcid, "parent_place_dcid": "Earth",
                                  "child_place_type": "Country", "date": "latest"})
        except UNDCError as exc:
            calls.append({"variable": dcid, "error": str(exc)[:200]})
            continue
        m = measure(r)
        m["variable"] = dcid
        calls.append(m)
        for row in ((r.get("entityMetadata") or {}).get("rows") or []):
            seen.add(row[0])
            if row[1] and row[0] not in names:
                names[row[0]] = row[1]
        for row in ((r.get("data") or {}).get("rows") or []):
            seen.add(row[0])
        if not quiet:
            still = sum(1 for p in seen if p not in names)
            print(f"  {dcid.split('/', 1)[-1]:<40} {m['entities']:>4} entities "
                  f"{m['named']:>4} named  first unnamed {m['first_unnamed'] or '-':<12} "
                  f"tail {'clean' if m['alphabetical_tail'] else 'MIXED'}   "
                  f"union {len(names)}, still unnamed {still}", file=sys.stderr)

    unnamed = sorted(p for p in seen if p not in names)
    out = {"generated": dt.date.today().isoformat(),
           "endpoint": client.endpoint,
           "places_seen": len(seen), "places_named": len(names),
           "unnamed": unnamed,
           "calls": calls,
           "names": dict(sorted(names.items()))}
    if not check_only:
        CACHE.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def render(out):
    measured = [c for c in out["calls"] if "entities" in c]
    capped = [c for c in measured if c["unnamed"]]
    caps = sorted(c["named"] for c in capped)
    today = out["generated"]
    lines = [
        "---", "layout: default", f"title: Country names per call — {today}", "---", "",
        f"# Country names per call — {today}", "",
        "`get_child_observations` over `Earth` / `Country` names each child place in its "
        "`entityMetadata` block — up to a point. Past it the name is an empty string, and "
        "the places dropped are the alphabetical tail by DCID. This table is that cap, "
        "measured on every call the build made, so the number is read off the platform "
        "rather than recalled.", "",
        f"**{len(measured)} calls · {len(capped)} returned at least one unnamed place · "
        f"names cap between {caps[0] if caps else '-'} and {caps[-1] if caps else '-'} "
        f"per call.** Union across calls: **{out['places_named']} of {out['places_seen']}** "
        f"distinct places named; {len(out['unnamed'])} still without a name.", "",
        "| Variable | Entities | Named | Unnamed | First unnamed | Tail alphabetical |",
        "|---|---:|---:|---:|---|---|",
    ]
    for c in measured:
        lines.append(f"| `{c['variable']}` | {c['entities']} | {c['named']} | {c['unnamed']} "
                     f"| {('`' + c['first_unnamed'] + '`') if c['first_unnamed'] else '—'} "
                     f"| {'yes' if c['alphabetical_tail'] else '**no**'} |")
    errs = [c for c in out["calls"] if "error" in c]
    if errs:
        lines += ["", "## Calls that errored", ""] + [f"- `{c['variable']}`: {c['error']}" for c in errs]
    if out["unnamed"]:
        lines += ["", "## Still unnamed after the union", "",
                  ", ".join(f"`{p}`" for p in out["unnamed"])]
    lines += ["", "## Reproducing", "", "```bash", "python3 probe/country_names.py", "```", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--budget", type=int, default=60,
                    help="maximum calls; the walk stops early once every place seen has a name")
    ap.add_argument("--check", action="store_true", help="measure only; write nothing")
    args = ap.parse_args()

    out = build(Client(pause=0.3), args.budget, check_only=args.check)
    text = render(out)
    if args.check:
        print(text)
        return
    today = out["generated"]
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / f"country-names-{today}.json").write_text(
        json.dumps({k: v for k, v in out.items() if k != "names"}, indent=1) + "\n",
        encoding="utf-8")
    (ARTIFACTS / f"country-names-{today}.md").write_text(text, encoding="utf-8")
    (ARTIFACTS / "country-names-latest.md").write_text(text, encoding="utf-8")
    print(f"wrote probe/cache/country_names.json ({out['places_named']} names) and "
          f"docs/artifacts/country-names-{today}.md")
    if out["unnamed"]:
        print(f"still unnamed: {len(out['unnamed'])} -- {' '.join(out['unnamed'][:12])}")


if __name__ == "__main__":
    main()
