#!/usr/bin/env python3
"""Check this repo's own crosswalk against the comparability spec.

A spec nobody validates against is a blog post. This asserts the structural
requirements and the conformance rules from
https://sarapis.github.io/undatacommons-nyc/spec/ -- including the ones a JSON
Schema cannot express, like "a reason must name a difference rather than restate
the grade".

Usage:  python3 probe/validate_crosswalk.py
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CROSSWALK = ROOT / "probe" / "crosswalk.json"

GRADES = {"DIRECT", "PROXY", "CONTEXT", "RANK-ONLY", "BLOCKED", "NO-SOURCE", "NO-SIGNAL"}
CHARTABLE = {"DIRECT", "PROXY"}
TIERS = {1, 2, 3}


def check(pairs):
    errs, warns = [], []
    seen = set()
    for p in pairs:
        pid = p.get("id", "<no id>")
        if pid in seen:
            errs.append(f"{pid}: duplicate id")
        seen.add(pid)

        grade = p.get("grade")
        if grade not in GRADES:
            errs.append(f"{pid}: grade {grade!r} not in the vocabulary")
        if p.get("tier") not in TIERS:
            errs.append(f"{pid}: tier {p.get('tier')!r} must be 1, 2 or 3")

        reason = (p.get("reason") or "").strip()
        if grade != "DIRECT" and len(reason) < 20:
            errs.append(f"{pid}: non-DIRECT grade requires a reason")
        # R4: the reason is the durable artifact, so it must say something the
        # grade does not already say.
        if reason and grade and reason.lower().strip(". ").replace("-", " ") == \
                grade.lower().replace("-", " "):
            errs.append(f"{pid}: reason merely restates the grade")

        if not p.get("un") and not p.get("comparator"):
            errs.append(f"{pid}: no comparator side recorded")

        # A non-chartable grade with no local side is fine (NO-SOURCE); a
        # chartable one without it is not.
        if grade in CHARTABLE and not p.get("nyc") and not p.get("local"):
            errs.append(f"{pid}: graded {grade} but records no local side")

        # Spec section 3: method class is a required FIELD on each side, not a
        # phrase in the prose. An earlier version of this check read the reason
        # text, which is exactly the kind of proxy-for-the-real-thing the spec
        # exists to discourage.
        for side_key in ("un", "comparator", "nyc", "local"):
            side = p.get(side_key)
            if isinstance(side, dict) and not side.get("method_class"):
                warns.append(f"{pid}: {side_key} side declares no method_class")
    return errs, warns


def main():
    doc = json.loads(CROSSWALK.read_text())
    pairs = doc.get("pairs", [])
    errs, warns = check(pairs)

    counts = {}
    for p in pairs:
        counts[p.get("grade")] = counts.get(p.get("grade"), 0) + 1

    print(f"crosswalk: {len(pairs)} pairs")
    for g, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {g:<12} {n}")
    print()
    for w in warns:
        print(f"  WARN  {w}")
    for e in errs:
        print(f"  ERROR {e}")
    print(f"\n{'CONFORMS' if not errs else 'DOES NOT CONFORM'} to comparability spec v0.1"
          f" ({len(errs)} errors, {len(warns)} warnings)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
