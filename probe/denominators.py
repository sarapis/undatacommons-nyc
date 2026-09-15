#!/usr/bin/env python3
"""Which cities can we actually produce a rate for?

Most SDG indicators are rates per 100,000, so a chart needs a population
denominator. For US cities that is Census ACS 1-year, which only publishes for
places above roughly 65,000 people. This matches municipal portals from the
inventory to ACS places and says which cities clear the bar.

A wrong denominator produces a rate that looks exactly like a right one, so this
refuses to guess: a portal whose city name matches more than one ACS place, or
matches none cleanly, is reported as ambiguous rather than assigned. (Spec v0.1
R5 -- ambiguity resolves to candidates, never to a guess.)

    python3 probe/denominators.py

Writes cities/denominators.json.
"""

import json
import os
import pathlib
import re
import ssl
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "portals" / "inventory.json"
OUT = ROOT / "cities" / "denominators.json"

# Domain fragments that reveal the state, used to disambiguate shared city names.
STATE_IN_DOMAIN = {
    "ma.gov": "25", "ma.us": "25", "-ma.": "25", "mass": "25",
    "oh.gov": "39", "-oh.": "39", "ohio": "39",
    "wa.gov": "53", "wa.us": "53", "wa.": "53",
    "ca.us": "06", "ca.gov": "06", "californ": "06",
    "ny.gov": "36", "nyc": "36", "cityofnewyork": "36",
    "tx.gov": "48", "texas": "48", "il.gov": "17", "pa.gov": "42",
    "va.gov": "51", "ri.gov": "44", "az.gov": "04", "fl.gov": "12",
    "wi.us": "55", "mi.gov": "26", "co.gov": "08", "ga.gov": "13",
}


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def census_key():
    k = os.environ.get("CENSUS_API_KEY")
    if k:
        return k
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("CENSUS_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("CENSUS_API_KEY needed: https://api.census.gov/data/key_signup.html")


def acs_places(year=2023):
    url = (f"https://api.census.gov/data/{year}/acs/acs1"
           f"?get=NAME,B01003_001E&for=place:*&key={census_key()}")
    with urllib.request.urlopen(url, timeout=120, context=_ctx()) as r:
        rows = json.loads(r.read().decode())[1:]
    out = []
    for name, pop, state, place in rows:
        bare = re.sub(r"\s+(city|town|village|CDP|municipality|borough|urban county)$",
                      "", name.split(",")[0]).strip()
        out.append({"name": bare, "key": bare.lower(), "state": state, "place": place,
                    "population": int(pop) if pop.lstrip("-").isdigit() else None,
                    "label": name})
    return out


# ACS is US-only, so a portal on a foreign TLD cannot have an ACS denominator
# no matter what its name looks like. This is what actually rules out Calgary.
NON_US_TLD = (".ca", ".uk", ".es", ".it", ".br", ".au", ".ch", ".dk", ".mx",
              ".de", ".fr", ".nl", ".se", ".no", ".fi", ".ar", ".cl", ".co",
              ".pt", ".ie", ".gr", ".ua", ".hr", ".be", ".at", ".nz", ".jp")

# Domains concatenate: "cityofchicago", "sanjoseca", "cityofberkeley". A place
# name may begin right after one of these, which is not a word boundary but is
# just as reliable a signal.
PREFIXES = ("cityof", "city", "data", "opendata", "open", "portal", "datahub",
            "citydata", "performance", "transparent", "fiscalfocus", "covid",
            "my", "www", "cos", "gov", "stat")

# What may legitimately follow a city name in a domain: a state postal code
# ("austintexas", "cambridgema"), or a platform/suffix word ("dallasopendata").
US_POSTAL = ("al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi",
             "id", "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi",
             "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc",
             "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut",
             "vt", "va", "wa", "wv", "wi", "wy")
STATE_WORDS = ("texas", "california", "florida", "ohio", "washington", "virginia",
               "massachusetts", "illinois", "arizona", "colorado", "oregon")
SUFFIXES = ("gov", "org", "com", "net", "us", "info", "data", "opendata",
            "govstat", "portal", "open", "ca", "socrata", "demo")


def candidates_for(portal, title, places):
    """ACS places whose name appears as a WORD in the domain or title.

    Substring matching is not safe here: 'calgary' contains 'gary', and matching
    Calgary (pop ~1.3M, Canada) to Gary, Indiana (pop 68k) would have produced a
    denominator twenty times too small and a rate that looked perfectly normal.
    """
    hay = re.sub(r"[^a-z0-9]+", " ", f"{portal} {title}".lower())
    tokens = set(hay.split())
    # also the domain with separators stripped, for "cityofnewyork"/"sanjoseca"
    squashed = hay.replace(" ", "")
    hits = []
    for p in places:
        n = p["key"]
        if len(n) < 4:
            continue
        if n in tokens:
            hits.append((p, "token"))
        elif " " in n and n.replace(" ", "") in squashed:
            hits.append((p, "squashed"))
        else:
            flat = n.replace(" ", "")
            if len(flat) < 4:
                continue
            for m in re.finditer(re.escape(flat), squashed):
                before = squashed[:m.start()]
                after = squashed[m.end():]
                # Accept only at a real boundary or right after a known prefix,
                # and never mid-word: "datacalgaryca" must not yield "gary".
                starts_ok = (not before or before.endswith(PREFIXES))
                ends_ok = (not after or not after[0].isalpha()
                           or after.startswith(SUFFIXES)
                           or after.startswith(STATE_WORDS)
                           or after[:2] in US_POSTAL)
                if starts_ok and ends_ok:
                    hits.append((p, "prefix"))
                    break
    return hits


def resolve(portal, title, places):
    host = portal.lower().rstrip("/")
    if any(host.endswith(t) for t in NON_US_TLD):
        return None, f"non-US domain ({host.rsplit('.', 1)[-1]}); ACS does not cover it"
    hits = candidates_for(portal, title, places)
    if not hits:
        return None, "no ACS place matches this portal name"
    if len(hits) > 1:
        # Try the state hinted by the domain before declaring ambiguity.
        low = f"{portal} {title}".lower()
        for frag, st in STATE_IN_DOMAIN.items():
            if frag in low:
                narrowed = [h for h in hits if h[0]["state"] == st]
                if len(narrowed) == 1:
                    return narrowed[0][0], None
        names = sorted({f"{h[0]['label']}" for h in hits})
        if len(names) > 1:
            return None, "ambiguous: " + "; ".join(names[:4])
    return hits[0][0], None


def main():
    inv = json.loads(INVENTORY.read_text())["rows"]
    muni = [r for r in inv if r.get("datasets") and r["level"] in ("city", "city-or-region")]
    places = acs_places()
    print(f"{len(muni)} municipal portals · {len(places)} ACS 1-year places", file=sys.stderr)

    ready, ambiguous, no_denominator = [], [], []
    for r in muni:
        place, why = resolve(r["portal"], r.get("title", ""), places)
        row = {"portal": r["portal"], "url": r["url"], "platform": r["platform"],
               "datasets": r["datasets"]}
        if place:
            row.update({"city": place["name"], "state_fips": place["state"],
                        "place_fips": place["place"], "population": place["population"],
                        "denominator": f"Census ACS 1-year B01003_001E, "
                                       f"place {place['place']} / state {place['state']}"})
            ready.append(row)
        elif why and why.startswith("ambiguous"):
            row["reason"] = why
            ambiguous.append(row)
        else:
            row["reason"] = why
            no_denominator.append(row)

    ready.sort(key=lambda r: -r["datasets"])
    OUT.write_text(json.dumps({"ready": ready, "ambiguous": ambiguous,
                               "no_denominator": no_denominator}, indent=1))

    print(f"\nchartable today (portal + ACS denominator): {len(ready)}")
    for r in ready[:20]:
        print(f"   {r['datasets']:>6}  {r['city']:<16} pop {r['population']:>9,}  {r['portal']}")
    print(f"\nambiguous city name, needs a human: {len(ambiguous)}")
    for r in ambiguous:
        print(f"   {r['portal']:<34} {r['reason'][:64]}")
    print(f"\nno ACS denominator (non-US, or under the 65k ACS-1yr floor): "
          f"{len(no_denominator)}")


if __name__ == "__main__":
    main()
