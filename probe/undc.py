"""Minimal client for the UN System Data Commons MCP server.

Stdlib only, on purpose: collaborators should be able to run the probe with a
bare `python3` and no virtualenv.

The server speaks streamable HTTP and answers statelessly, so every call is a
self-contained JSON-RPC POST. Responses come back as SSE frames; we parse the
`data:` lines out rather than pulling in an SSE library.
"""

import json
import ssl
import time
import urllib.error
import urllib.request

ENDPOINT = "https://unsd-datacommons.gcp.un-icc.cloud/mcp"

# The server's own instructions forbid guessing DCIDs and require that every
# datapoint keep its attribution. Both rules are enforced by how this client is
# used, not by the client itself -- see coverage_probe.py.
GOVERNED_PREFIX = "undata/"


class UNDCError(RuntimeError):
    pass


def _ssl_context():
    """Trust store that works on stock macOS python.org builds.

    Those ship without root certificates unless you run Install Certificates.command,
    so a plain default context raises CERTIFICATE_VERIFY_FAILED even though curl is
    fine. Prefer certifi when it is importable and fall back to the default.
    """
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


class Client:
    def __init__(self, endpoint=ENDPOINT, pause=0.4, timeout=120):
        self.endpoint = endpoint
        self.pause = pause          # be a polite guest; no documented rate limit
        self.timeout = timeout
        self._ssl = _ssl_context()
        self._id = 0

    def _rpc(self, method, params=None):
        self._id += 1
        payload = json.dumps(
            {"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}}
        ).encode()
        req = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout, context=self._ssl) as resp:
                body = resp.read().decode()
        except urllib.error.HTTPError as exc:
            raise UNDCError(f"{method} -> HTTP {exc.code}: {exc.read()[:300]!r}") from exc
        except urllib.error.URLError as exc:
            if "CERTIFICATE_VERIFY_FAILED" in str(exc.reason):
                raise UNDCError(
                    "TLS verification failed. Run `pip3 install certifi`, or on macOS run "
                    "/Applications/Python\\ 3.x/Install\\ Certificates.command"
                ) from exc
            raise UNDCError(f"{method} -> {exc.reason}") from exc
        time.sleep(self.pause)
        return self._parse_sse(body, method)

    @staticmethod
    def _parse_sse(body, method):
        for line in body.splitlines():
            if not line.startswith("data: "):
                continue
            frame = json.loads(line[6:])
            if "error" in frame:
                raise UNDCError(f"{method} -> {frame['error']}")
            return frame.get("result", {})
        raise UNDCError(f"{method} -> no data frame in response")

    def call_tool(self, name, arguments):
        result = self._rpc("tools/call", {"name": name, "arguments": arguments})
        return result.get("structuredContent", {})

    # --- the three tools the probe needs ---------------------------------

    def search_indicators(self, query, places=None, limit=10):
        args = {"query": query, "per_search_limit": limit}
        if places:
            args["places"] = places
        return self.call_tool("search_indicators", args)

    def get_observations(self, variable_dcid, place_dcid, date="all"):
        return self.call_tool(
            "get_observations",
            {"variable_dcid": variable_dcid, "place_dcid": place_dcid, "date": date},
        )

    def list_tools(self):
        return [t["name"] for t in self._rpc("tools/list").get("tools", [])]
