"""Harvest live Socrata domains by paging the Discovery catalog.

The documented /domains endpoint is retired (404), so this collects the domain
off each result instead. The catalog caps resultSetSize at 10,000, so this is a
large sample rather than a census -- stated as such.
"""
import json, ssl, sys, time, urllib.parse, urllib.request, collections
try:
    import certifi; CTX=ssl.create_default_context(cafile=certifi.where())
except ImportError: CTX=ssl.create_default_context()
BASE="https://api.us.socrata.com/api/catalog/v1"
domains=collections.Counter()
seen=0
for off in range(0, 10000, 100):
    qs=urllib.parse.urlencode({"only":"dataset","limit":100,"offset":off})
    try:
        with urllib.request.urlopen(f"{BASE}?{qs}",timeout=60,context=CTX) as r:
            d=json.loads(r.read().decode())
    except Exception as e:
        print(f"  ! offset {off}: {e}", file=sys.stderr); time.sleep(2); continue
    res=d.get("results") or []
    if not res: break
    for x in res:
        dom=(x.get("metadata") or {}).get("domain")
        if dom: domains[dom]+=1
    seen+=len(res)
    if off % 1000 == 0:
        print(f"  {seen} results, {len(domains)} domains", file=sys.stderr)
    time.sleep(0.15)
json.dump(dict(domains), open("socrata_domains.json","w"))
print(f"\nsampled {seen} datasets across {len(domains)} distinct Socrata domains")
