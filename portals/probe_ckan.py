"""Verify which candidate portals are live CKAN instances.

No global CKAN registry exists -- ckan.org's instance page and dataportals.org's
API are both 404, and opendatainception.io serves a broken payload. So the only
honest way to inventory CKAN is to take a candidate list and fingerprint each
one: /api/3/action/status_show returns the CKAN version when it is CKAN and not
blocked.
"""
import csv, json, ssl, sys, urllib.parse, urllib.request, concurrent.futures as cf
try:
    import certifi; CTX=ssl.create_default_context(cafile=certifi.where())
except ImportError: CTX=ssl.create_default_context()

rows=list(csv.DictReader(open("portals.csv")))
cands=[]
for r in rows:
    u=(r.get("url") or "").strip().rstrip("/")
    if u.startswith("http"):
        cands.append((u, r.get("title","").strip(), r.get("country","").strip(),
                      (r.get("publisher_classification") or "").strip()))

def check(c):
    url,title,country,cls=c
    try:
        req=urllib.request.Request(f"{url}/api/3/action/status_show",
                                   headers={"User-Agent":"undatacommons-nyc portal survey"})
        with urllib.request.urlopen(req,timeout=12,context=CTX) as r:
            d=json.loads(r.read().decode())
        v=(d.get("result") or {}).get("ckan_version")
        if v: return {"url":url,"title":title,"country":country,"class":cls,"ckan":v}
    except Exception:
        pass
    return None

live=[]
with cf.ThreadPoolExecutor(max_workers=16) as ex:
    for i,res in enumerate(ex.map(check,cands),1):
        if res: live.append(res)
        if i%100==0: print(f"  probed {i}/{len(cands)} · {len(live)} live CKAN", file=sys.stderr)
json.dump(live,open("ckan_live.json","w"),indent=1)
print(f"\n{len(live)} confirmed live CKAN of {len(cands)} candidates")
