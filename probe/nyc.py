"""Minimal NYC Open Data (Socrata) client.

Stdlib only, matching undc.py. No app token: the anonymous tier is rate-limited
but fine for probe volumes. Set SOCRATA_APP_TOKEN in the environment to raise it.
"""

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request

CATALOG = "https://api.us.socrata.com/api/catalog/v1"
DOMAIN = "data.cityofnewyork.us"


class NYCError(RuntimeError):
    pass


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def _get(url, params, timeout=90):
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{qs}")
    token = os.environ.get("SOCRATA_APP_TOKEN")
    if token:
        req.add_header("X-App-Token", token)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise NYCError(f"HTTP {exc.code}: {exc.read()[:250]!r}") from exc
    except urllib.error.URLError as exc:
        raise NYCError(str(exc.reason)) from exc


def metadata(dataset_id):
    """Catalog record for one dataset -- name, last update, and whether it is archived."""
    d = _get(CATALOG, {"domains": DOMAIN, "ids": dataset_id, "limit": 1})
    results = d.get("results") or []
    if not results:
        raise NYCError(f"{dataset_id} not found in the {DOMAIN} catalog")
    res = results[0].get("resource", {})
    name = res.get("name") or ""
    return {
        "id": res.get("id"),
        "name": name,
        "updated_at": (res.get("updatedAt") or "")[:10],
        # NYC marks retired datasets by renaming them rather than removing them,
        # so a dataset can keep answering queries long after it stopped updating.
        "archived": name.upper().startswith("ARCHIVED"),
        "type": res.get("type"),
    }


def query(dataset_id, soql):
    """Run a SoQL query and return the rows."""
    return _get(f"https://{DOMAIN}/resource/{dataset_id}.json", soql)
