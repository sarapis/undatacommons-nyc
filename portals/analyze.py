#!/usr/bin/env python3
"""Merge the Socrata and CKAN surveys into one inventory, with live counts.

The two harvests answer different questions -- which Socrata domains exist, and
which CKAN candidates still respond -- and neither is a table you can reason
over. This joins them, asks each portal how many datasets it actually holds, and
classifies the level of government, so the inventory can be read rather than
grepped.

    python3 portals/analyze.py

Writes portals/inventory.json and docs/artifacts/portals-latest.md.
"""

import concurrent.futures as cf
import datetime as dt
import json
import pathlib
import re
import ssl
import sys
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SOCRATA_CATALOG = "https://api.us.socrata.com/api/catalog/v1"

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

# A heuristic, and stated as one -- the point is to separate municipal portals
# from regional and national ones well enough to count them. Order matters:
# national beats regional beats county beats city, because "data.ny.gov" would
# otherwise match a city rule on "ny".

US_STATES = set("""al ak az ar ca co ct de fl ga hi id il in ia ks ky la me md ma mi mn ms
mo mt ne nv nh nj nm ny nc nd oh ok or pa ri sc sd tn tx ut vt va wa wv wi wy dc""".split())

# Several portals spell the state out: data.texas.gov, data.michigan.gov.
US_STATE_NAMES = set("""alabama alaska arizona arkansas california colorado connecticut
delaware florida georgia hawaii idaho illinois indiana iowa kansas kentucky louisiana
maine maryland massachusetts michigan minnesota mississippi missouri montana nebraska
nevada newhampshire newjersey newmexico newyork northcarolina northdakota ohio oklahoma
oregon pennsylvania rhodeisland southcarolina southdakota tennessee texas utah vermont
virginia washington westvirginia wisconsin wyoming""".split())

# Sub-national regions that are not US states: Italian regioni, German Länder,
# Canadian provinces, Australian states, Brazilian estados.
REGIONS = ("toscana", "emilia-romagna", "trentino", "lombardia", "piemonte", "veneto",
           "puglia", "sicilia", "sardegna", "nrw", "bayern", "berlin.de", "hamburg",
           "novascotia", "alberta", "ontario", "quebec", "bc.ca", "gnb.",
           "nsw.gov", "vic.gov", "qld.gov", "sa.gov.au", "aragon", "andalucia",
           "catalunya", "euskadi", "galicia", "rs.gov.br", "pr.gov.br", "ba.gov.br",
           "bayareametro", "metro.", "mtc.ca.gov")

NATIONAL = ("datos.gov.co", "catalogodatos.gub.uy", "datos.gob.cl", "datos.gob.es",
            "opendata.swiss", "canada.ca", "europa.eu", "gov.uk", "data.gov.au",
            "cdc.gov", "transportation.gov", "commerce.gov", "hud.gov", "energy.gov",
            "nasa", "usaid", "noaa", "epa.gov", "va.gov", "hhs.gov", "gsa.gov")

COUNTY = ("county", "countyof", "condado", "smcgov", "cookcountyil", "kingcounty",
          "maricopa", "riverside", "sonoma", "montgomery")

# Municipal markers: generic words for "city" in several languages, plus the
# city names that actually appear in this inventory.
CITY_WORDS = ("cityof", "cityofnew", "citydata", "citywide", "prefeitura", "comune",
              "ciudad", "stadt", "ville", "kommune", "gemeente", "municipio",
              "municipal", "datamill")
CITY_NAMES = ("chicago", "boston", "sanjose", "seattle", "austin", "dallas", "oakland",
              "mesaaz", "cambridgema", "winnipeg", "nola", "kcmo", "calgary", "edmonton",
              "madrid", "milano", "matera", "buenosaires", "fortaleza", "pbh", "recife",
              "brla", "kirkland", "leeds", "baltimore", "philadelphia", "denver",
              "louisville", "nashville", "memphis", "raleigh", "charlotte", "detroit",
              "pittsburgh", "hartford", "providence", "syracuse", "rochester", "buffalo",
              "albuquerque", "tucson", "fresno", "sacramento", "longbeach", "anaheim",
              "bloomington", "tempe", "scottsdale", "gilbertaz", "chandler", "glendale",
              "montgomeryal", "asheville", "greensboro", "durham", "chattanooga",
              "lacity", "zagreb", "karlsruhe", "richmond", "everettwa", "norfolk",
              "cincinnati", "sustainablesm", "santamonica", "tucson", "boise",
              "lincoln", "wichita", "tacoma", "spokane", "reno", "orlando", "tampa",
              "stpete", "jerseycity", "newark", "yonkers", "arlington", "alexandria")


def level(domain, title=""):
    d = f"{domain} {title}".lower()
    host = domain.lower()

    for pat in NATIONAL:
        if pat in d:
            return "national"
    # data.gov.ua / datos.gob.mx / opendata.gov.je -- national portals by shape
    if re.search(r"(?:data|datos|dados|opendata)\.(?:gov|gob)\.[a-z]{2}$", host):
        return "national"
    # data.<state>.gov / healthdata.<state>.gov / opendata.<state>.gov
    m = re.search(r"(?:^|\.)([a-z]{2})\.gov$", host)
    if m and m.group(1) in US_STATES:
        return "state"
    if re.search(r"\.state\.[a-z]{2}\.us", host) or "opendata.maryland" in host:
        return "state"
    for pat in REGIONS:
        if pat in d:
            return "state"
    for pat in COUNTY:
        if pat in d:
            return "county"
    for pat in CITY_WORDS:
        if pat in d:
            return "city"
    for pat in CITY_NAMES:
        if pat in d:
            return "city"
    if host.endswith(".edu") or "cuny" in host or "socrata.com" in host:
        return "other"
    return "unclassified"


def _get(url, params=None, timeout=20):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "portal inventory survey"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return json.loads(r.read().decode())


def socrata_count(domain):
    try:
        d = _get(SOCRATA_CATALOG, {"domains": domain, "only": "dataset", "limit": 1})
        return d.get("resultSetSize"), None
    except Exception as exc:                       # noqa: BLE001
        return None, f"{type(exc).__name__}"


def ckan_count(url):
    """Ask a CKAN portal how many datasets it holds.

    The official catalog lists http:// URLs recorded years ago, so a bare
    request misses portals that now require https. A failure here means "did not
    answer an anonymous package_search", NOT "is dead" -- data.gov and
    govdata.de are plainly alive and both refuse this probe.
    """
    base = url.rstrip("/")
    candidates = [base]
    if base.startswith("http://"):
        candidates.append("https://" + base[len("http://"):])
    last = None
    for b in candidates:
        try:
            d = _get(f"{b}/api/3/action/package_search", {"rows": 1})
            n = (d.get("result") or {}).get("count")
            if n is not None:
                return n, None
        except Exception as exc:                   # noqa: BLE001
            last = f"{type(exc).__name__}"
    return None, last


def main():
    soc = json.loads((HERE / "socrata-domains.json").read_text())
    ckan = json.loads((HERE / "ckan-live.json").read_text())
    # The official CKAN Ecosystem Catalog list (ckan/ckan-instances on GitHub),
    # which we initially and wrongly reported as non-existent -- the registries
    # we probed first were its dead predecessors.
    official = json.loads((HERE / "ckan-instances-official.json").read_text())

    rows = []
    for dom in soc:
        rows.append({"portal": dom, "url": f"https://{dom}", "platform": "socrata",
                     "country": "", "title": "", "version": "", "source": "socrata-catalog"})
    for c in ckan:
        rows.append({"portal": urllib.parse.urlparse(c["url"]).netloc, "url": c["url"],
                     "platform": "ckan", "country": c.get("country", ""),
                     "title": c.get("title", ""), "version": c.get("ckan", ""),
                     "source": "okfn-probed"})
    seen = {r["portal"] for r in rows}
    for x in official:
        host = urllib.parse.urlparse(x.get("url", "")).netloc
        if not host or host in seen:
            continue
        seen.add(host)
        facets = {f.get("key"): f.get("value") for f in (x.get("facets") or [])}
        rows.append({"portal": host, "url": x["url"].rstrip("/"), "platform": "ckan",
                     "country": "", "title": x.get("title", ""), "version": "",
                     "source": "ckan-ecosystem",
                     "declared_type": facets.get("Type", ""),
                     "region": facets.get("Region", "")})

    print(f"querying {len(rows)} portals for live dataset counts...", file=sys.stderr)

    def enrich(r):
        n, err = (socrata_count(r["portal"]) if r["platform"] == "socrata"
                  else ckan_count(r["url"]))
        r["datasets"] = n
        r["error"] = err
        declared = (r.get("declared_type") or "").lower()
        if "local" in declared or "regional" in declared:
            r["level"] = "city-or-region"
        elif "national" in declared:
            r["level"] = "national"
        elif declared:
            r["level"] = {"academic": "other", "community": "other",
                          "other organizations": "other"}.get(declared, "other")
        else:
            r["level"] = level(r["portal"], r["title"])
        return r

    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        rows = list(ex.map(enrich, rows))

    live = [r for r in rows if r.get("datasets")]
    live.sort(key=lambda r: -(r["datasets"] or 0))

    today = dt.date.today().isoformat()
    (HERE / "inventory.json").write_text(json.dumps(
        {"surveyed": today, "portals": len(rows), "responding": len(live),
         "rows": rows}, indent=1))

    by_level, by_platform = {}, {}
    for r in live:
        by_level[r["level"]] = by_level.get(r["level"], 0) + 1
        by_platform[r["platform"]] = by_platform.get(r["platform"], 0) + 1
    cities = [r for r in live if r["level"] == "city"]

    md = ["---", "layout: default", f"title: Portal inventory — {today}", "---", "",
          f"# City open data portal inventory — {today}", "",
          "**There is no global registry of open data portals.** Socrata's `/domains` endpoint, "
          "`ckan.org/about/instances`, the dataportals.org API and opendatainception all return "
          "404 or broken payloads, and data.gov and data.gov.uk block their CKAN APIs. This "
          "inventory is therefore *constructed* — harvested from Socrata's Discovery catalog and "
          "fingerprinted for CKAN — and has to be re-verified rather than looked up.", "",
          f"- **{len(rows)}** portals surveyed · **{len(live)}** responding with a dataset count",
          f"- by platform: " + " · ".join(f"**{v}** {k}" for k, v in
                                          sorted(by_platform.items(), key=lambda kv: -kv[1])),
          f"- by level: " + " · ".join(f"**{v}** {k}" for k, v in
                                       sorted(by_level.items(), key=lambda kv: -kv[1])),
          f"- total datasets across responding portals: "
          f"**{sum(r['datasets'] for r in live):,}**", "",
          "Level is a crude domain/title heuristic — it separates municipal portals from state and "
          "national ones well enough to count them, and will misclassify edge cases.", "",
          "## Municipal portals", "",
          "| Datasets | Portal | Platform | Country | Version |", "|---:|---|---|---|---|"]
    for r in cities:
        md.append(f"| {r['datasets']:,} | [{r['portal']}]({r['url']}) | {r['platform']} | "
                  f"{r['country']} | {r['version']} |")

    md += ["", "## All responding portals", "",
           "| Datasets | Portal | Platform | Level |", "|---:|---|---|---|"]
    for r in live:
        md.append(f"| {r['datasets']:,} | [{r['portal']}]({r['url']}) | {r['platform']} | "
                  f"{r['level']} |")

    dead = [r for r in rows if not r.get("datasets")]
    md += ["", f"## Not responding ({len(dead)})", "",
           "Reachable when first surveyed, or listed in a registry, but returning no count now. "
           "Link rot in this space is severe and ongoing.", "",
           "| Portal | Platform | Error |", "|---|---|---|"]
    for r in dead:
        md.append(f"| {r['portal']} | {r['platform']} | {r.get('error') or 'no count'} |")
    md.append("")

    out = ROOT / "docs" / "artifacts" / f"portals-{today}.md"
    out.write_text("\n".join(md))
    (ROOT / "docs" / "artifacts" / "portals-latest.md").write_text("\n".join(md))

    print(f"\n{len(rows)} surveyed, {len(live)} responding, {len(cities)} municipal")
    print(f"  by level:    {by_level}")
    print(f"  by platform: {by_platform}")
    print(f"  wrote portals/inventory.json + docs/artifacts/portals-{today}.md")


if __name__ == "__main__":
    main()
