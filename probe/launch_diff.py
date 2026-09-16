#!/usr/bin/env python3
"""The launch diff — has the platform moved under us?

The UN System Data Commons goes fully public on 17 Sep 2026. Everything this
project publishes was measured against the pre-launch deployment, so the open
question recorded in the briefing is blunt: *will staging DCIDs survive the
public launch?* A renamed or withdrawn DCID does not raise an error. It returns
an empty result, which reads exactly like a country that does not report --
and the demo would show a blank chart to a room at Google NY.

So this takes a snapshot and diffs it against the last one. Three layers:

  1. ENDPOINT  which host answers, and which tools it exposes
  2. VARIABLE  every DCID the crosswalk names, resolved through MCP metadata --
               catches a rename or a redefinition even where data still flows
  3. SERIES    every (variable, place) the crosswalk and its peer comparators
               depend on, fetched and compared value by value

plus a set diff of the enumerated SDG corpus, which catches DCIDs appearing or
vanishing outside the twelve pairs we happen to have graded.

Every row is printed, always. Four of this project's six worst bugs were caught
by printing a table across all cases and reading it, and hidden by a summary
count that said everything passed.

Usage:
  python3 probe/launch_diff.py                     snapshot + diff vs baseline
  python3 probe/launch_diff.py --set-baseline      record this snapshot as the baseline
  python3 probe/launch_diff.py --corpus PATH       compare corpus against PATH instead
                                                   of the list stored in the baseline
Writes docs/artifacts/launch-diff-<date>.{json,md}; baseline in
probe/cache/launch-baseline.json.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from undc import Client, UNDCError, ENDPOINT, GOVERNED_PREFIX  # noqa: E402
import corpus as corpus_mod                                     # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "probe" / "cache"
ARTIFACTS = ROOT / "docs" / "artifacts"
BASELINE = CACHE / "launch-baseline.json"
CORPUS = CACHE / "corpus.json"

# A value that moves by less than this is a float-formatting difference, not a
# revision. Anything at or above it is reported.
VALUE_EPSILON = 1e-9


def rest_alive(url):
    """Is the REST node endpoint answering at all? Structural walks need it."""
    try:
        req = urllib.request.Request(url + "?nodes=undata/topic/Root&property=->relevantVariable")
        with urllib.request.urlopen(req, timeout=60, context=corpus_mod._ctx()) as r:
            return {"status": r.status, "ok": r.status == 200}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "ok": False}
    except Exception as exc:                                     # noqa: BLE001
        return {"status": None, "ok": False, "error": str(exc)}


def crosswalk_targets(spec):
    """Every (variable, place) the crosswalk depends on, peers included.

    Peers are what the demo's world-position cards compare against, so a peer
    series that stops resolving breaks a published card just as surely as the
    headline one does.
    """
    entities, series = {}, []
    for pair in spec["pairs"]:
        un = pair.get("un") or {}
        dcid = un.get("dcid")
        if not dcid:
            continue
        places = [p for p in [un.get("place")] + list(un.get("peers") or []) if p]
        entities.setdefault(dcid, set()).update(places)
        for place in places:
            series.append((dcid, place, pair["id"]))
    return {d: sorted(e) for d, e in sorted(entities.items())}, series


def fetch_metadata(client, entities_by_var):
    """Metadata per variable, asked about the entities the crosswalk uses it for.

    `entity_dcids` is NOT optional. Omit it and the server answers 200 with an
    empty structuredContent -- no error, no status field, nothing -- and a
    caller that trusts the shape records every variable as withdrawn from the
    graph. The first run of this script did exactly that and claimed all twelve
    crosswalk DCIDs had disappeared, two days before the launch it was written
    to check. One call per variable, so a short answer means absent rather than
    truncated; the response cap is variables x entities together.
    """
    out = {}
    for dcid, ents in entities_by_var.items():
        try:
            r = client.call_tool("get_variable_metadata",
                                 {"variable_dcids": [dcid], "entity_dcids": ents})
        except UNDCError as exc:
            out[dcid] = {"status": "ERROR", "error": str(exc)}
            continue
        if not r:
            out[dcid] = {"status": "NO-RESPONSE",
                         "error": "empty structuredContent — check the argument shape"}
            continue
        m = (r.get("variables") or {}).get(dcid)
        if not m:
            out[dcid] = {"status": "MISSING"}
            continue
        facets = m.get("facets") or []
        if not facets:
            out[dcid] = {"status": "NO-FACETS", "name": m.get("name")}
            continue
        best = max(facets, key=lambda f: f.get("obsCount") or 0)
        props = best.get("properties") or {}
        dr = best.get("dateRange") or {}
        cov = sorted((best.get("scope") or {}).get("entityCoverage") or [])
        out[dcid] = {"status": "OK", "name": m.get("name"),
                     "unit": (props.get("unit") or "").split("UNIT_MEASURE-")[-1],
                     "observation_period": props.get("observationPeriod"),
                     "obs_count": best.get("obsCount"),
                     "date_range": f"{str(dr.get('start', ''))[:4]}-{str(dr.get('end', ''))[:4]}",
                     "provenance": best.get("provenanceId"),
                     "entities_asked": list(ents),
                     "entity_coverage": cov,
                     "n_facets": len(facets)}
    return out


def fetch_series(client, dcid, place):
    """One series, reduced to what a diff can compare."""
    try:
        o = client.get_observations(dcid, place, date="all")
    except UNDCError as exc:
        return {"status": "ERROR", "error": str(exc)}
    rows = (o.get("data") or {}).get("rows") or []
    if not rows:
        # The dangerous case. An empty result is what a withdrawn DCID returns,
        # and also what a country that does not report returns. Same shape.
        return {"status": "EMPTY", "n_obs": 0}
    src = o.get("sourceMetadata") or {}
    values = {str(r[1])[:4]: r[2] for r in rows}
    years = sorted(int(y) for y in values if y.isdigit())
    return {"status": "OK", "name": (o.get("variable") or {}).get("name"),
            "n_obs": len(rows), "first": years[0] if years else None,
            "last": years[-1] if years else None,
            "unit": (src.get("unit") or "").split("UNIT_MEASURE-")[-1],
            "provenance": src.get("provenanceUrl"), "values": values}


def snapshot(client, spec, corpus_path):
    entities_by_var, series = crosswalk_targets(spec)

    print(f"endpoint {ENDPOINT}", file=sys.stderr)
    try:
        tools = client.list_tools()
    except UNDCError as exc:
        tools = {"error": str(exc)}
    print(f"  tools: {tools}", file=sys.stderr)

    print(f"resolving metadata for {len(entities_by_var)} variables...", file=sys.stderr)
    meta = fetch_metadata(client, entities_by_var)
    for d, m in meta.items():
        print(f"  {m['status']:<10} {d}", file=sys.stderr)

    print(f"fetching {len(series)} series...", file=sys.stderr)
    fetched = {}
    for i, (dcid, place, pair_id) in enumerate(series, 1):
        fetched[f"{dcid}@{place}"] = dict(fetch_series(client, dcid, place), pair=pair_id)
        print(f"  {i}/{len(series)} {pair_id} {place} "
              f"{fetched[f'{dcid}@{place}']['status']}", file=sys.stderr)

    bases = []
    if corpus_path and pathlib.Path(corpus_path).exists():
        bases = sorted(json.loads(pathlib.Path(corpus_path).read_text()).get("bases", {}))

    ungoverned = sorted(d for d in entities_by_var if not d.startswith(GOVERNED_PREFIX))
    return {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "endpoint": {"mcp": ENDPOINT, "tools": tools,
                     "rest": rest_alive(corpus_mod.REST)},
        "variables": meta,
        "series": fetched,
        "corpus": {"source": str(corpus_path), "base_indicators": bases},
        "ungoverned_dcids_in_crosswalk": ungoverned,
    }


# --- diffing -------------------------------------------------------------

def diff_series(old, new):
    """Compare one series two ways: does it still resolve, and did it change?"""
    if old is None:
        return "NEW", "not in baseline"
    if new is None:
        return "DROPPED", "no longer requested"
    if old["status"] != new["status"]:
        return "STATUS", f"{old['status']} -> {new['status']}"
    if new["status"] != "OK":
        return "same", new["status"]

    notes = []
    if old.get("n_obs") != new.get("n_obs"):
        notes.append(f"n_obs {old.get('n_obs')} -> {new.get('n_obs')}")
    if (old.get("first"), old.get("last")) != (new.get("first"), new.get("last")):
        notes.append(f"span {old.get('first')}–{old.get('last')} -> "
                     f"{new.get('first')}–{new.get('last')}")
    if old.get("unit") != new.get("unit"):
        notes.append(f"unit `{old.get('unit')}` -> `{new.get('unit')}`")
    if old.get("name") != new.get("name"):
        notes.append(f"name `{old.get('name')}` -> `{new.get('name')}`")
    if old.get("provenance") != new.get("provenance"):
        notes.append("provenance URL changed")

    ov, nv = old.get("values") or {}, new.get("values") or {}
    revised = []
    for y in sorted(set(ov) & set(nv)):
        a, b = ov[y], nv[y]
        try:
            if abs(float(a) - float(b)) >= VALUE_EPSILON:
                revised.append(f"{y}: {a} -> {b}")
        except (TypeError, ValueError):
            if a != b:
                revised.append(f"{y}: {a!r} -> {b!r}")
    if revised:
        notes.append("values revised — " + "; ".join(revised[:6])
                     + (f" (+{len(revised) - 6} more)" if len(revised) > 6 else ""))

    return ("CHANGED" if notes else "same"), ("; ".join(notes) or "identical")


def diff(base, cur):
    rows = []
    keys = sorted(set(base.get("series", {})) | set(cur.get("series", {})))
    for k in keys:
        verdict, note = diff_series(base.get("series", {}).get(k),
                                    cur.get("series", {}).get(k))
        rows.append({"key": k, "pair": (cur.get("series", {}).get(k)
                                        or base["series"][k]).get("pair"),
                     "status": (cur.get("series", {}).get(k) or {}).get("status", "—"),
                     "verdict": verdict, "note": note})

    var_rows = []
    for d in sorted(set(base.get("variables", {})) | set(cur.get("variables", {}))):
        o, n = base.get("variables", {}).get(d), cur.get("variables", {}).get(d)
        if o is None:
            v, note = "NEW", "not in baseline"
        elif n is None:
            v, note = "DROPPED", "no longer requested"
        elif o.get("status") != n.get("status"):
            v, note = "STATUS", f"{o.get('status')} -> {n.get('status')}"
        else:
            bits = [f"{f} `{o.get(f)}` -> `{n.get(f)}`"
                    for f in ("name", "unit", "observation_period", "obs_count",
                              "date_range", "provenance", "entity_coverage", "n_facets")
                    if o.get(f) != n.get(f)]
            v, note = ("CHANGED" if bits else "same"), ("; ".join(bits) or "identical")
        var_rows.append({"dcid": d, "status": (n or {}).get("status", "—"),
                         "verdict": v, "note": note})

    ob = set(base.get("corpus", {}).get("base_indicators") or [])
    nb = set(cur.get("corpus", {}).get("base_indicators") or [])
    corpus_diff = {"baseline_count": len(ob), "current_count": len(nb),
                   "added": sorted(nb - ob), "removed": sorted(ob - nb)}

    ot = base.get("endpoint", {}).get("tools")
    nt = cur.get("endpoint", {}).get("tools")
    endpoint_diff = {
        "mcp_host_changed": base.get("endpoint", {}).get("mcp") != cur.get("endpoint", {}).get("mcp"),
        "tools_baseline": ot, "tools_current": nt, "tools_changed": ot != nt,
        "rest": cur.get("endpoint", {}).get("rest"),
    }
    return {"series": rows, "variables": var_rows,
            "corpus": corpus_diff, "endpoint": endpoint_diff}


def _baseline_age_hours(base, cur):
    try:
        b = dt.datetime.fromisoformat(base["generated"])
        c = dt.datetime.fromisoformat(cur["generated"])
    except (KeyError, TypeError, ValueError):
        return None
    return (c - b).total_seconds() / 3600.0


def render(base, cur, d):
    today = dt.date.today().isoformat()
    bad = [r for r in d["series"] if r["verdict"] not in ("same",)]
    empty = [r for r in d["series"] if r["status"] == "EMPTY"]
    errored = [r for r in d["series"] if r["status"] == "ERROR"]
    varbad = [r for r in d["variables"] if r["verdict"] != "same"]

    md = ["---", "layout: default", f"title: Launch diff — {today}", "---", "",
          f"# Launch diff — {today}", "",
          f"Baseline taken {base.get('generated', '—')} · this run {cur['generated']}.", "",
          f"Endpoint `{cur['endpoint']['mcp']}`"
          + (" — **HOST CHANGED since baseline**" if d["endpoint"]["mcp_host_changed"] else "")
          + ".", ""]

    clean = (not bad and not varbad and not d["corpus"]["added"]
             and not d["corpus"]["removed"] and not d["endpoint"]["tools_changed"])
    verdict = ("**No drift.** Every DCID the crosswalk names still resolves to the same "
               "series, with the same values."
               if clean
               else "**Drift detected.** Rows marked other than `same` below are the ones "
                    "to read; nothing here is safe to summarise away.")
    md += [verdict, ""]

    # A "no drift" verdict against a baseline recorded minutes ago says almost
    # nothing, and read out of context it looks like proof the platform held.
    # Say so on the page rather than letting the reader assume otherwise.
    age = _baseline_age_hours(base, cur)
    if clean and age is not None and age < 1:
        md += [f"The baseline this is compared against was recorded "
               f"{int(round(age * 60))} minute(s) before this run, so it establishes the "
               "**baseline** rather than proving anything held over time. The claim it "
               "supports is that the snapshot is reproducible; the interesting comparison is "
               "the next run against it.", ""]

    md += [
           f"- {len(d['series'])} series checked · {len(bad)} changed · "
           f"{len(empty)} empty · {len(errored)} errored",
           f"- {len(d['variables'])} variables checked · {len(varbad)} changed",
           f"- corpus {d['corpus']['baseline_count']} -> {d['corpus']['current_count']} "
           f"base indicators · {len(d['corpus']['added'])} added · "
           f"{len(d['corpus']['removed'])} removed",
           f"- tools: {d['endpoint']['tools_current']}"
           + (" — **CHANGED**" if d["endpoint"]["tools_changed"] else ""),
           f"- REST node endpoint: "
           + ("answering" if (d["endpoint"]["rest"] or {}).get("ok") else "**NOT ANSWERING**"),
           "", "## Series", "",
           "Every (variable, place) the crosswalk and its peer comparators depend on. "
           "An `EMPTY` status is the dangerous one — a withdrawn DCID and a country that "
           "does not report are the same shape.", "",
           "| Pair | Variable @ place | Status | Verdict | Detail |", "|---|---|---|---|---|"]
    for r in d["series"]:
        dcid, _, place = r["key"].rpartition("@")
        note = r["note"] if len(r["note"]) <= 120 else r["note"][:117] + "..."
        md.append(f"| {r['pair']} | `{dcid}` @ `{place}` | {r['status']} | "
                  f"{'`' + r['verdict'] + '`' if r['verdict'] != 'same' else 'same'} | {note} |")

    md += ["", "## Variables", "",
           "Resolved through `get_variable_metadata`, which catches a rename or a "
           "redefinition even where observations still flow.", "",
           "| DCID | Status | Verdict | Detail |", "|---|---|---|---|"]
    for r in d["variables"]:
        note = r["note"] if len(r["note"]) <= 120 else r["note"][:117] + "..."
        md.append(f"| `{r['dcid']}` | {r['status']} | "
                  f"{'`' + r['verdict'] + '`' if r['verdict'] != 'same' else 'same'} | {note} |")

    md += ["", "## Corpus", "",
           f"SDG base indicators enumerated: **{d['corpus']['baseline_count']}** at baseline, "
           f"**{d['corpus']['current_count']}** now.", ""]
    if d["corpus"]["added"]:
        md += [f"**Added ({len(d['corpus']['added'])}):**", "",
               "\n".join(f"- `{x}`" for x in d["corpus"]["added"][:60]), ""]
    if d["corpus"]["removed"]:
        md += [f"**Removed ({len(d['corpus']['removed'])}):** every one of these is a DCID "
               "the enumeration found before and does not find now.", "",
               "\n".join(f"- `{x}`" for x in d["corpus"]["removed"][:60]), ""]
    if not d["corpus"]["added"] and not d["corpus"]["removed"]:
        md += ["No indicator appeared or vanished.", ""]

    if cur.get("ungoverned_dcids_in_crosswalk"):
        md += ["", "## Ungoverned DCIDs", "",
               "These are named by the crosswalk but do not carry the governed "
               f"`{GOVERNED_PREFIX}` prefix:", "",
               "\n".join(f"- `{x}`" for x in cur["ungoverned_dcids_in_crosswalk"]), ""]

    return "\n".join(md) + "\n"



# --- self-test -----------------------------------------------------------

def self_test():
    """Prove the diff reports drift, using a mutated copy of the baseline.

    A diff that returns "no change" is indistinguishable from a diff that
    cannot see change, and this project has shipped that mistake six times. So
    every drift class this script claims to catch is injected deliberately and
    asserted. No network: it mutates the stored snapshot.
    """
    import copy
    base = json.loads(BASELINE.read_text())
    cur = copy.deepcopy(base)

    ok_keys = [k for k, v in base["series"].items() if v["status"] == "OK"]
    empty_keys = [k for k, v in base["series"].items() if v["status"] == "EMPTY"]
    if not ok_keys or not empty_keys:
        print("self-test needs a baseline with both OK and EMPTY series", file=sys.stderr)
        return 1

    cases = []

    # A value silently revised by the publisher.
    k = ok_keys[0]
    y = sorted(cur["series"][k]["values"])[0]
    cur["series"][k]["values"][y] = float(cur["series"][k]["values"][y]) + 1.0
    cases.append(("value revised", "series", k, "values revised"))

    # A DCID withdrawn: still answers, now with nothing. The launch-day risk.
    k = ok_keys[1]
    cur["series"][k] = {"status": "EMPTY", "n_obs": 0, "pair": base["series"][k]["pair"]}
    cases.append(("series went EMPTY", "series", k, "OK -> EMPTY"))

    # A country that starts reporting.
    k = empty_keys[0]
    cur["series"][k] = dict(base["series"][k], status="OK", n_obs=3, first=2000,
                            last=2002, unit="X", values={"2000": 1.0})
    cases.append(("series became OK", "series", k, "EMPTY -> OK"))

    # Unit changed underneath an unchanged number -- the one that makes a chart lie.
    k = ok_keys[2]
    cur["series"][k]["unit"] = "TOTALLY_DIFFERENT_UNIT"
    cases.append(("unit changed", "series", k, "unit"))

    # Years dropped off the end of a series.
    k = ok_keys[3]
    last = str(cur["series"][k]["last"])
    cur["series"][k]["values"].pop(last, None)
    cur["series"][k]["n_obs"] -= 1
    cur["series"][k]["last"] = cur["series"][k]["last"] - 1
    cases.append(("span shortened", "series", k, "span"))

    # A variable renamed or redefined while its data keeps flowing.
    vk = sorted(cur["variables"])[0]
    cur["variables"][vk] = dict(cur["variables"][vk], name="Renamed indicator")
    cases.append(("variable renamed", "variables", vk, "name"))

    # A variable withdrawn from the graph entirely.
    vk2 = sorted(cur["variables"])[1]
    cur["variables"][vk2] = {"status": "MISSING"}
    cases.append(("variable MISSING", "variables", vk2, "OK -> MISSING"))

    # An indicator vanishing from the enumerated corpus.
    dropped = cur["corpus"]["base_indicators"].pop(0)
    cases.append(("corpus indicator removed", "corpus", dropped, "removed"))

    # A tool disappearing from the server.
    cur["endpoint"]["tools"] = list(cur["endpoint"]["tools"])[:-1]
    cases.append(("tool removed", "endpoint", "tools", "changed"))

    d = diff(base, cur)
    srows = {r["key"]: r for r in d["series"]}
    vrows = {r["dcid"]: r for r in d["variables"]}

    print(f"{'injected':<28}{'where':<12}{'caught':<8}evidence")
    failures = 0
    for label, where, key, expect in cases:
        if where == "series":
            r = srows.get(key, {})
            caught = r.get("verdict") != "same" and expect in r.get("note", "")
            evidence = f"{r.get('verdict')}: {r.get('note', '')[:52]}"
        elif where == "variables":
            r = vrows.get(key, {})
            caught = r.get("verdict") != "same"
            evidence = f"{r.get('verdict')}: {r.get('note', '')[:52]}"
        elif where == "corpus":
            caught = key in d["corpus"]["removed"]
            evidence = f"removed list holds {len(d['corpus']['removed'])}"
        else:
            caught = d["endpoint"]["tools_changed"]
            evidence = f"tools_changed={d['endpoint']['tools_changed']}"
        failures += not caught
        print(f"{label:<28}{where:<12}{'yes' if caught else 'NO':<8}{evidence}")

    # And the converse: an unmutated copy must report nothing.
    clean = diff(base, json.loads(BASELINE.read_text()))
    quiet = (not [r for r in clean["series"] if r["verdict"] != "same"]
             and not [r for r in clean["variables"] if r["verdict"] != "same"]
             and not clean["corpus"]["added"] and not clean["corpus"]["removed"]
             and not clean["endpoint"]["tools_changed"])
    print(f"{'unmutated copy stays quiet':<28}{'all':<12}{'yes' if quiet else 'NO':<8}"
          f"no rows reported")
    failures += not quiet

    print(f"\n{len(cases) + 1 - failures}/{len(cases) + 1} self-test checks passed")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set-baseline", action="store_true",
                    help="record this snapshot as the baseline and stop")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the diff detects drift, by mutating the baseline")
    ap.add_argument("--corpus", default=str(CORPUS),
                    help="corpus.json to read the current base-indicator list from")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    spec = json.loads((ROOT / "probe" / "crosswalk.json").read_text())
    cur = snapshot(Client(), spec, args.corpus)

    if args.set_baseline or not BASELINE.exists():
        BASELINE.write_text(json.dumps(cur, indent=1))
        print(f"\nwrote baseline {BASELINE}"
              + ("" if args.set_baseline else " (none existed; nothing to diff against yet)"),
              file=sys.stderr)
        if args.set_baseline:
            return 0

    base = json.loads(BASELINE.read_text())
    d = diff(base, cur)

    today = dt.date.today().isoformat()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / f"launch-diff-{today}.json").write_text(
        json.dumps({"baseline": base.get("generated"), "current": cur["generated"],
                    "diff": d, "snapshot": cur}, indent=1))
    text = render(base, cur, d)
    (ARTIFACTS / f"launch-diff-{today}.md").write_text(text)
    (ARTIFACTS / "launch-diff-latest.md").write_text(text)

    drifted = [r for r in d["series"] if r["verdict"] != "same"]
    varbad = [r for r in d["variables"] if r["verdict"] != "same"]
    print(f"\n{'Pair':<22}{'Place':<16}{'Status':<8}{'Verdict':<10}Detail")
    for r in d["series"]:
        dcid, _, place = r["key"].rpartition("@")
        print(f"{str(r['pair']):<22}{place:<16}{r['status']:<8}{r['verdict']:<10}"
              f"{r['note'][:60]}")
    print(f"\nseries: {len(d['series'])} checked, {len(drifted)} drifted")
    print(f"variables: {len(d['variables'])} checked, {len(varbad)} drifted")
    print(f"corpus: {d['corpus']['baseline_count']} -> {d['corpus']['current_count']}, "
          f"+{len(d['corpus']['added'])} -{len(d['corpus']['removed'])}")
    print(f"wrote docs/artifacts/launch-diff-{today}.md")
    return 1 if (drifted or varbad or d["corpus"]["added"] or d["corpus"]["removed"]) else 0


if __name__ == "__main__":
    sys.exit(main())
