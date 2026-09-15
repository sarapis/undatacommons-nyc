#!/usr/bin/env python3
"""Smoke test: exercise every tool and check figures against the published demo.

The server and the demo must not drift apart. These expected values are the ones
on https://sarapis.github.io/undatacommons-nyc/demo/benchmarks.html
"""
import json
import pathlib
import subprocess
import sys

SERVER = str(pathlib.Path(__file__).resolve().parent / "server.py")


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


def main():
    out = rpc([
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        call(2, "benchmark", {"indicator": "pm25", "year": "2019"}),
        call(3, "benchmark", {"indicator": "poverty"}),
        call(4, "world_position", {"indicator": "road-deaths", "year": "2021"}),
        call(5, "world_position", {"indicator": "municipal-waste", "year": "2019"}),
        call(6, "benchmark", {"indicator": "municipal waste"}),
    ])
    checks = []
    sc = lambda i: out[i]["result"]["structuredContent"]  # noqa: E731

    checks.append(("4 tools exposed", len(out[1]["result"]["tools"]) == 4))
    b = sc(2)
    checks.append(("pm25 2019 NYC 6.6", round(b["nyc"]["value"], 1) == 6.6))
    checks.append(("pm25 2019 comparator 7.57", round(b["comparator"]["value"], 2) == 7.57))
    checks.append(("poverty refused", sc(3).get("refused") is True))
    r = sc(4)
    checks.append(("road deaths rank 18 of 196", (r["rank"], r["of"]) == (18, 196)))
    w = sc(5)
    checks.append(("municipal waste rank 41 of 91", (w["rank"], w["of"]) == (41, 91)))
    checks.append(("municipal waste ~397.9 kg", abs(w["nyc_value"] - 397.9) < 0.5))
    checks.append(("ambiguous name returns candidates", "candidates" in sc(6)))

    for label, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    bad = [l for l, ok in checks if not ok]
    print(f"\n{len(checks) - len(bad)}/{len(checks)} passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
