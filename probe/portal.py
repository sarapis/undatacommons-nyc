#!/usr/bin/env python3
"""One interface over Socrata and CKAN open data portals.

The NYC pipeline talks to Socrata directly. Every other city is a coin flip
between Socrata and CKAN, so the catalog fetch has to be platform-agnostic
before any of this generalises.

Both platforms are reachable anonymously; both rate-limit, and CKAN portals vary
enormously in which extensions they run, so the adapter asks only for fields
every CKAN ships.
"""

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request

SOCRATA_CATALOG = "https://api.us.socrata.com/api/catalog/v1"


class PortalError(RuntimeError):
    pass


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def _get(url, params=None, timeout=60, token=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "undatacommons-nyc multi-city crosswalk bootstrapper"})
    if token:
        req.add_header("X-App-Token", token)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise PortalError(f"HTTP {exc.code} for {url[:110]}") from exc
    except Exception as exc:                                  # noqa: BLE001
        raise PortalError(f"{type(exc).__name__}: {exc}") from exc


class Portal:
    """A city's open data catalog, normalised.

    `catalog()` yields dicts with the same keys regardless of platform:
    id, name, description, updated, columns, tags, category, url.
    """

    def __init__(self, city):
        self.key = city["key"]
        self.name = city["name"]
        self.platform = city["platform"]
        self.domain = city["domain"].rstrip("/")
        self.city = city

    # -- Socrata ---------------------------------------------------------
    def _socrata(self, limit):
        rows, offset = [], 0
        token = os.environ.get("SOCRATA_APP_TOKEN")
        while len(rows) < limit:
            d = _get(SOCRATA_CATALOG, {"domains": self.domain, "only": "dataset",
                                       "limit": min(100, limit - len(rows)),
                                       "offset": offset}, token=token)
            got = d.get("results") or []
            if not got:
                break
            for r in got:
                res = r.get("resource", {}) or {}
                cls = r.get("classification", {}) or {}
                rows.append({
                    "id": res.get("id"),
                    "name": res.get("name") or "",
                    "description": (res.get("description") or "")[:1500],
                    "updated": (res.get("updatedAt") or "")[:10],
                    "columns": (res.get("columns_name") or [])[:40],
                    "column_descriptions": [c for c in (res.get("columns_description") or [])[:40] if c],
                    "tags": (cls.get("domain_tags") or [])[:12],
                    "category": cls.get("domain_category") or "",
                    "url": r.get("permalink") or "",
                })
            offset += len(got)
            if offset >= (d.get("resultSetSize") or 0):
                break
        return rows

    # -- CKAN ------------------------------------------------------------
    def _ckan(self, limit):
        rows, start = [], 0
        while len(rows) < limit:
            d = _get(f"{self.domain}/api/3/action/package_search",
                     {"rows": min(100, limit - len(rows)), "start": start})
            result = d.get("result") or {}
            got = result.get("results") or []
            if not got:
                break
            for p in got:
                # CKAN nests field names inside resources, not on the package,
                # and most portals do not publish them at all. Take what exists.
                cols = []
                for res in (p.get("resources") or [])[:5]:
                    for f in (res.get("fields") or [])[:20]:
                        if isinstance(f, dict) and f.get("id"):
                            cols.append(f["id"])
                rows.append({
                    "id": p.get("name") or p.get("id"),
                    "name": p.get("title") or p.get("name") or "",
                    "description": (p.get("notes") or "")[:1500],
                    "updated": (p.get("metadata_modified") or "")[:10],
                    "columns": cols[:40],
                    "column_descriptions": [],
                    "tags": [t.get("name") for t in (p.get("tags") or [])[:12]
                             if isinstance(t, dict) and t.get("name")],
                    "category": ((p.get("groups") or [{}])[0].get("title")
                                 if p.get("groups") else "") or "",
                    "url": f"{self.domain}/dataset/{p.get('name')}",
                })
            start += len(got)
            if start >= (result.get("count") or 0):
                break
        return rows

    def catalog(self, limit=3000):
        if self.platform == "socrata":
            return self._socrata(limit)
        if self.platform == "ckan":
            return self._ckan(limit)
        raise PortalError(f"unsupported platform {self.platform!r}")

    def size(self):
        """Total datasets, without pulling the whole catalog."""
        if self.platform == "socrata":
            d = _get(SOCRATA_CATALOG, {"domains": self.domain, "only": "dataset", "limit": 1})
            return d.get("resultSetSize") or 0
        d = _get(f"{self.domain}/api/3/action/package_search", {"rows": 1})
        return (d.get("result") or {}).get("count") or 0
