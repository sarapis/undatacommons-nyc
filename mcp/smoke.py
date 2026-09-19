#!/usr/bin/env python3
"""Smoke test: exercise every tool and check figures against the published demo.

The server and the demo must not drift apart. These expected values are the ones
on https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SERVER = str(ROOT / "mcp" / "server.py")
DEMO = ROOT / "demo" / "benchmarks.html"
DEMO_MIRROR = ROOT / "docs" / "demo" / "benchmarks.html"


def rpc(msgs):
    r = subprocess.run([sys.executable, SERVER],
                       input="\n".join(json.dumps(m) for m in msgs) + "\n",
                       capture_output=True, text=True, timeout=300)
    if r.stderr.strip():
        print("stderr:", r.stderr[:300], file=sys.stderr)
    return {json.loads(l)["id"]: json.loads(l) for l in r.stdout.splitlines()}


def call(i, name, args):
    return {"jsonrpc": "2.0", "id": i, "method": "tools/call",
            "params": {"name": name, "arguments": args}}


def demo_checks():
    """The demo's US-silent table against the worksheet that produced it.

    The twelve rows are generated from docs/artifacts/us-silent-*.json but live
    in hand-authored HTML, so nothing stops the two drifting apart the next time
    either is touched. This is the same rule as the figures above: the server and
    the demo must not disagree, and neither must the demo and the artifact.
    """
    checks = []
    arts = sorted((ROOT / "docs" / "artifacts").glob("us-silent-*.json"))
    if not arts:
        return [("us-silent artifact present", False)]
    o = json.loads(arts[-1].read_text())
    html = DEMO.read_text()
    core = [r for r in o["indicators"] if re.search(r"waste|wetland|water", r["name"], re.I)]
    checks.append(("demo and mirror identical", DEMO.read_text() == DEMO_MIRROR.read_text()))

    # The world strips: every country the platform can name is named. The only blanks
    # allowed are the places no call ever names (probe/country_names.py lists them).
    cache_path = ROOT / "probe" / "cache" / "country_names.json"
    checks.append(("country-name cache present", cache_path.exists()))
    if cache_path.exists():
        never = set(json.loads(cache_path.read_text(encoding="utf-8"))["unnamed"])
        m = re.search(r"const WORLD = (\{.*?\});\n", html, re.S)
        blanks = {f"country/{row[0]}" for card in json.loads(m.group(1)).values()
                  for row in card["vals"] if not row[1]} if m else {"parse failed"}
        checks.append(("demo world strips: every nameable country is named",
                       blanks <= never))
        if not blanks <= never:
            print("   blank:", ", ".join(sorted(blanks - never)), file=sys.stderr)
    checks.append((f"{len(core)} waste/water rows in the worksheet", len(core) == 12))
    missing = [r for r in core if r["dcid"].rsplit("/", 1)[-1] not in html]
    checks.append(("every waste series appears in the demo", not missing))
    # the country counts printed next to each series must match the artifact
    bad = []
    for r in core:
        series = r["dcid"].rsplit("/", 1)[-1]
        m = re.search(re.escape(series) + r"</span></td>\s*<td class=\"numcell\"><b>(\d+)</b>",
                      html)
        if not m or int(m.group(1)) != r["world"]["countries"]:
            bad.append(f"{series}: demo {m.group(1) if m else '?'} vs artifact "
                       f"{r['world']['countries']}")
    checks.append(("reporting-country counts match the artifact", not bad))
    if bad:
        print("   drift:", "; ".join(bad), file=sys.stderr)
    checks.append(("no US observations in any of the twelve",
                   all(r["world"]["us_obs"] == 0 for r in core)))

    # The masthead funnel. It read "248 with US data, 377 have none" for three
    # days -- numbers that matched no run and did not even sum to 689 -- because
    # nothing tied them to the pipeline. Now something does.
    screened = json.loads((ROOT / "probe" / "cache" / "screened.json").read_text())
    usable = [x for x in screened["indicators"]
              if x.get("grade") in ("GREEN", "AMBER", "RANK-ONLY")]
    silent = sum(1 for x in usable if not x.get("us_reports"))
    pairs = len(json.loads((ROOT / "probe" / "crosswalk.json").read_text())["pairs"])
    for label, value in (("corpus", len(screened["indicators"])), ("usable", len(usable)),
                         ("US-silent", silent), ("crosswalk pairs", pairs)):
        checks.append((f"funnel {label} = {value}", f"<dd>{value}</dd>" in html))
    checks.append((f"funnel names {len(screened['indicators']) - len(usable)} too thin",
                   f"{len(screened['indicators']) - len(usable)} are too thin" in html))

    # The two category-gap blocks, against probe/category_gaps.py's output.
    gaps = sorted((ROOT / "docs" / "artifacts").glob("category-gaps-*.json"))
    if not gaps:
        checks.append(("category-gaps artifact present", False))
        return checks
    g = json.loads(gaps[-1].read_text())
    el, fo = g["categories"]["elections"], g["categories"]["records access"]
    checks.append(("elections: framework count is zero", el["n_framework"] == 0))
    checks.append((f"elections: 0 of {g['named_indicators']} on the page",
                   f"<span class=\"big\">0 of {g['named_indicators']}</span>" in html))
    checks.append((f"elections: {el['n_datasets']} datasets / {el['n_cities']} cities on the page",
                   f"{el['n_datasets']} datasets &middot; {el['n_cities']} cities" in html))
    checks.append((f"records access: {fo['n_datasets']} logs / {fo['n_cities']} cities on the page",
                   f"{fo['n_datasets']} logs &middot; {fo['n_cities']} cities" in html))
    checks.append(("records access: exactly one framework indicator", fo["n_framework"] == 1))
    pr = g["categories"].get("procurement")
    checks.append(("procurement category measured", pr is not None))
    if pr:
        checks.append((f"procurement: {pr['n_datasets']} datasets / {pr['n_cities']} cities on the page",
                       f"{pr['n_datasets']} datasets &middot; {pr['n_cities']} cities" in html))
        empty = [c for c in pr["unnamed_dcid_candidates"]
                 if c["dcid"].rsplit("/", 1)[-1].startswith("SG_SCP_PROCN")]
        checks.append(("procurement: SDG 12.7.1 slots exist and are empty",
                       len(empty) == 3 and all(c["observations"] == 0 for c in empty)))
    waste = [k for n, k in el["nearest_offered"] if "waste" in n.lower()]
    checks.append(("elections' nearest-concept punchline matches the data",
                   bool(waste) and f"<strong>{waste[0]}</strong> of those election" in html))
    return checks


def main():
    out = rpc([
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        call(2, "benchmark", {"indicator": "pm25", "year": "2019"}),
        call(3, "benchmark", {"indicator": "poverty"}),
        call(4, "world_position", {"indicator": "road-deaths", "year": "2021"}),
        call(5, "world_position", {"indicator": "municipal-waste", "year": "2019"}),
        call(6, "benchmark", {"indicator": "municipal waste"}),
        call(7, "framework_coverage", {"concept": "election voting turnout"}),
        call(8, "reportable_gaps", {"theme": "waste", "limit": 5}),
        call(9, "data_quality", {"dcid": "VC_SNS_WALN_DRK"}),
    ])
    checks = []
    sc = lambda i: out[i]["result"]["structuredContent"]  # noqa: E731

    checks.append(("7 tools exposed", len(out[1]["result"]["tools"]) == 7))
    b = sc(2)
    checks.append(("pm25 2019 NYC 6.6", round(b["nyc"]["value"], 1) == 6.6))
    checks.append(("pm25 2019 comparator 7.57", round(b["comparator"]["value"], 2) == 7.57))
    checks.append(("poverty refused", sc(3).get("refused") is True))
    r = sc(4)
    checks.append(("road deaths rank 18 of 196", (r["rank"], r["of"]) == (18, 196)))
    w = sc(5)
    checks.append(("municipal waste rank 41 of 91", (w["rank"], w["of"]) == (41, 91)))
    checks.append(("municipal waste ~397.9 kg", abs(w["nyc_value"] - 397.9) < 0.5))
    # The platform names ~155 places per call and drops the rest; the server fills them
    # from probe/cache/country_names.json. A neighbour that reads "country/USA" means the
    # cache is missing or stale (python3 probe/country_names.py).
    checks.append(("world_position: no neighbour is a bare DCID",
                   all(not n["place"].startswith("country/")
                       for n in r["neighbours"] + w["neighbours"])))
    checks.append(("ambiguous name returns candidates", "candidates" in sc(6)))

    fc = sc(7)
    checks.append(("framework_coverage: zero election indicators",
                   fc["matching_indicators"] == 0))
    checks.append(("framework_coverage: attaches the measured municipal side",
                   fc["municipal_side"].get("cities") == 23))
    rg = sc(8)
    checks.append(("reportable_gaps: every row ungraded",
                   all(r["graded"] is False for r in rg["indicators"])))
    checks.append(("reportable_gaps: municipal waste has 133 reporting countries",
                   any(r["reporting_countries"] == 133 for r in rg["indicators"])))
    dq = sc(9)
    checks.append(("data_quality: Kyrgyzstan flagged and verified",
                   dq["verified_error_series"] == 1
                   and dq["findings"][0]["value"] == 6710.0))
    checks += demo_checks()

    for label, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    bad = [l for l, ok in checks if not ok]
    print(f"\n{len(checks) - len(bad)}/{len(checks)} passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
