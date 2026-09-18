#!/usr/bin/env python3
"""Stage 1 — enumerate the governed corpus by walking the topic tree.

Answers the question the crosswalk should have started from: what is actually in
here? The first eleven pairs came from topics chosen out of my head, which meant
the crosswalk reflected assumptions about NYC's data rather than the UN's real
coverage. This replaces intuition with the denominator.

Walks `->relevantVariable` from `undata/topic/Root` via REST. That is one of the
five REST uses the platform guide sanctions (corpus orientation from an undata/
identifier); using REST to *search* is explicitly forbidden and we do not.

Resumable: state is checkpointed, so a long walk can be interrupted and resumed.

Usage:  python3 probe/corpus.py [--resume]
Writes probe/cache/corpus.json.
"""

import argparse
import json
import os
import pathlib
import ssl
import sys
import time
import urllib.parse
import urllib.request
from collections import deque

# Overridable for the same reason as the MCP endpoint -- see probe/undc.py.
REST = os.environ.get(
    "UNDC_REST", "https://unsd-datacommons.gcp.un-icc.cloud/core/api/v2/node")
ROOT = "undata/topic/Root"

# The corpus is reachable through three overlapping hierarchies -- the SDG goal
# framework, per-agency trees, and a themes tree -- so walking everything
# re-traverses the same variables through tens of thousands of duplicate topic
# nodes. A Voluntary Local Review reports against the SDG framework, so the 17
# goal trees are the principled default scope, not a shortcut. Use --roots all
# for the whole graph when you actually need it.
SDG_GOAL_ROOTS = [f"undata/topic/sdgf/goal-{i}" for i in range(1, 18)]
CACHE = pathlib.Path(__file__).resolve().parent / "cache"
CORPUS = CACHE / "corpus.json"
STATE = CACHE / "corpus-state.json"
BATCH = 20


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def base_indicator(dcid):
    """Collapse a disaggregation variant to its parent indicator.

    `undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY` -> `undata/sdg/EN_ATM_PM25`.
    A single indicator explodes into dozens of variables across sex, age,
    urbanization and wealth quintile; counting those as separate indicators
    would wildly overstate how much there is to crosswalk.
    """
    return dcid.split(".", 1)[0]


def resolve_members(groups, ctx=None):
    """Follow ->member from StatVarPeerGroup nodes to real variable DCIDs.

    The goal trees do not expose observation-bearing variables directly. They
    expose `undata/svpg/...` peer-group nodes (svpg = StatVarPeerGroup) whose
    `member` arc lists the actual DCIDs, e.g.
        undata/svpg/sdg/EN_ATM_PM25.001
          -> undata/sdg/EN_ATM_PM25.URBANIZATION--DOU_CITY

    We resolve rather than rewrite the prefix. Rewriting `svpg/sdg/X` to `sdg/X`
    would look right and is exactly the DCID guessing the platform forbids --
    and a guessed DCID returns an empty result, not an error.
    """
    ctx = ctx or _ctx()
    members, groups = set(), sorted(groups)
    for i in range(0, len(groups), BATCH):
        chunk = groups[i:i + BATCH]
        qs = [("nodes", g) for g in chunk] + [("property", "->member")]
        try:
            with urllib.request.urlopen(f"{REST}?{urllib.parse.urlencode(qs)}",
                                        timeout=90, context=ctx) as r:
                data = json.loads(r.read().decode())
        except Exception as exc:               # noqa: BLE001
            print(f"  ! {exc}", file=sys.stderr)
            time.sleep(2)
            continue
        for _, payload in (data.get("data") or {}).items():
            arc = (payload.get("arcs", {}).get("member") or {})
            for node in arc.get("nodes", []):
                if node.get("dcid"):
                    members.add(node["dcid"])
        print(f"  resolved {min(i + BATCH, len(groups))}/{len(groups)} groups "
              f"-> {len(members)} variables", file=sys.stderr)
        time.sleep(0.2)
    return members


def agency(dcid):
    parts = dcid.split("/")
    return parts[1] if dcid.startswith("undata/") and len(parts) > 2 else "other"


def walk(roots, resume=False, ctx=None, state_path=None):
    ctx = ctx or _ctx()
    state_path = state_path or STATE
    if resume and state_path.exists():
        st = json.loads(state_path.read_text())
        topics, variables = set(st["topics"]), set(st["variables"])
        seen, queue = set(st["seen"]), deque(st["queue"])
        print(f"resuming: {len(seen)} walked, {len(queue)} queued", file=sys.stderr)
    else:
        topics, variables, seen, queue = set(), set(), set(), deque(roots)

    since_checkpoint = 0
    while queue:
        batch = []
        while queue and len(batch) < BATCH:
            n = queue.popleft()
            if n not in seen:
                batch.append(n)
        if not batch:
            continue
        seen.update(batch)

        qs = [("nodes", d) for d in batch] + [("property", "->relevantVariable")]
        try:
            with urllib.request.urlopen(f"{REST}?{urllib.parse.urlencode(qs)}",
                                        timeout=90, context=ctx) as r:
                data = json.loads(r.read().decode())
        except Exception as exc:               # noqa: BLE001 - keep walking
            print(f"  ! {exc}", file=sys.stderr)
            time.sleep(2)
            continue

        for _, payload in (data.get("data") or {}).items():
            arc = (payload.get("arcs", {}).get("relevantVariable") or {})
            for node in arc.get("nodes", []):
                child = node.get("dcid")
                if not child:
                    continue
                if "/topic/" in child:
                    topics.add(child)
                    if child not in seen:
                        queue.append(child)
                else:
                    variables.add(child)

        since_checkpoint += len(batch)
        if since_checkpoint >= 500:
            state_path.write_text(json.dumps({"topics": sorted(topics),
                                              "variables": sorted(variables),
                                              "seen": sorted(seen), "queue": list(queue)}))
            since_checkpoint = 0
        print(f"  walked={len(seen):<6} topics={len(topics):<6} "
              f"vars={len(variables):<7} queue={len(queue)}", file=sys.stderr)
        time.sleep(0.2)

    return topics, variables


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--roots", choices=["sdg", "all"], default="sdg",
                    help="sdg = the 17 SDG goal trees (default); all = the whole graph")
    # Without this, --roots all overwrites the SDG corpus that screened.json,
    # the smell sweep, the US-silent worksheet, category_gaps and the demo's
    # funnel all resolve against -- a whole-graph walk would silently replace
    # the 689 with a different set and every downstream count would move.
    ap.add_argument("--out", default=None,
                    help="where to write (default: cache/corpus.json for --roots sdg, "
                         "cache/corpus-all.json for --roots all)")
    args = ap.parse_args()

    out_path = pathlib.Path(args.out) if args.out else (
        CORPUS if args.roots == "sdg" else CACHE / "corpus-all.json")
    # Resume state is per-output, so an interrupted whole-graph walk cannot be
    # resumed into the SDG corpus or vice versa.
    state_path = out_path.with_name(out_path.stem + "-state.json")

    CACHE.mkdir(parents=True, exist_ok=True)
    roots = SDG_GOAL_ROOTS if args.roots == "sdg" else [ROOT]
    print(f"walking {len(roots)} root(s): {args.roots}", file=sys.stderr)
    topics, raw = walk(roots, resume=args.resume, state_path=state_path)

    # Everything the goal trees yield is a peer-group node; the real variables
    # hang off its member arc.
    groups = {v for v in raw if v.startswith("undata/svpg/")}
    direct = raw - groups
    print(f"\nresolving {len(groups):,} peer groups...", file=sys.stderr)
    variables = direct | resolve_members(groups)

    bases = {}
    for v in sorted(variables):
        bases.setdefault(base_indicator(v), []).append(v)

    by_agency = {}
    for b in bases:
        by_agency[agency(b)] = by_agency.get(agency(b), 0) + 1

    out = {
        "walked_from": roots,
        "scope": args.roots,
        "topic_nodes": len(topics),
        "peer_groups": len(groups),
        "variables": len(variables),
        "base_indicators": len(bases),
        "base_indicators_by_agency": dict(sorted(by_agency.items(), key=lambda kv: -kv[1])),
        "bases": {b: vs for b, vs in sorted(bases.items())},
    }
    out_path.write_text(json.dumps(out, indent=1))
    if state_path.exists():
        state_path.unlink()

    print(f"\ntopic nodes      {len(topics):,}")
    print(f"peer groups      {len(groups):,}")
    print(f"variables        {len(variables):,}")
    print(f"base indicators  {len(bases):,}")
    print("by agency:", json.dumps(out["base_indicators_by_agency"], indent=1))
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
