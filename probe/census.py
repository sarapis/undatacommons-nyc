"""Census denominators for NYC rate calculations.

Most SDG indicators are rates per 100,000 while NYC publishes counts, so almost
every Tier 3 pair needs an annual population figure. This supplies one.

Requires a free key from https://api.census.gov/data/key_signup.html, read from
CENSUS_API_KEY (or a gitignored .env beside this repo). The key is never stored
in a tracked file.

KNOWN GAP: there is no ACS 1-year release for 2020 -- collection was disrupted by
COVID and the Bureau withheld the standard product. That is a real hole, not a
fetch failure, and it lands on a year of real interest (NYC homicides jumped that
year). We leave it empty rather than interpolating: an invented denominator
produces a rate that looks exactly like a measured one.
"""

import json
import os
import pathlib
import ssl
import urllib.error
import urllib.parse
import urllib.request

# NYC = place 51000 within state 36.
NYC_PLACE, NYC_STATE = "51000", "36"
TOTAL_POPULATION = "B01003_001E"
NO_ACS1 = {2020}


class CensusError(RuntimeError):
    pass


def _key():
    key = os.environ.get("CENSUS_API_KEY")
    if key:
        return key
    env = pathlib.Path(__file__).resolve().parent.parent / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("CENSUS_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise CensusError(
        "No CENSUS_API_KEY. Get a free key at "
        "https://api.census.gov/data/key_signup.html and export it, or put it in "
        ".env (gitignored). Never commit it -- this repo is public."
    )


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def nyc_population(years):
    """{year: population} for the years available. Missing years are simply absent."""
    key = _key()
    out, gaps = {}, []
    for year in years:
        if year in NO_ACS1:
            gaps.append(year)
            continue
        qs = urllib.parse.urlencode({
            "get": f"NAME,{TOTAL_POPULATION}",
            "for": f"place:{NYC_PLACE}",
            "in": f"state:{NYC_STATE}",
            "key": key,
        })
        url = f"https://api.census.gov/data/{year}/acs/acs1?{qs}"
        try:
            with urllib.request.urlopen(url, timeout=60, context=_ctx()) as r:
                rows = json.loads(r.read().decode())
            out[year] = int(rows[1][1])
        except urllib.error.HTTPError as exc:
            # A 404 means that vintage is not published, which is data news, not an error.
            if exc.code == 404:
                gaps.append(year)
                continue
            raise CensusError(f"ACS {year}: HTTP {exc.code}") from exc
        except (ValueError, IndexError, KeyError) as exc:
            raise CensusError(f"ACS {year}: unexpected response ({exc})") from exc
    return out, sorted(gaps)
