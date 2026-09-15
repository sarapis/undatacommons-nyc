#!/usr/bin/env python3
"""Attach a city name and country to each municipal portal.

The inventory is keyed by domain: Socrata entries were harvested from the
catalog and carry no title or country at all, and only 16 of 70 have a country
from the CKAN registry. This fills both in, recording WHERE each value came from
so a wrong one can be traced rather than trusted.

Priority for the city name: an ACS match (authoritative, US), then the project
registry, then a CKAN portal title, then the domain itself.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INV = ROOT / "portals/inventory.json"

TLD_COUNTRY = {
    "br": "Brazil", "it": "Italy", "es": "Spain", "ar": "Argentina", "mx": "Mexico",
    "cl": "Chile", "co": "Colombia", "uy": "Uruguay", "ca": "Canada", "au": "Australia",
    "nz": "New Zealand", "uk": "United Kingdom", "ie": "Ireland", "de": "Germany",
    "at": "Austria", "ch": "Switzerland", "nl": "Netherlands", "be": "Belgium",
    "dk": "Denmark", "se": "Sweden", "no": "Norway", "fi": "Finland", "fr": "France",
    "pt": "Portugal", "gr": "Greece", "hr": "Croatia", "cz": "Czechia", "pl": "Poland",
    "ua": "Ukraine", "tw": "Taiwan", "jp": "Japan", "eu": "European Union",
}
# Only .gov and .us are reliably US. Defaulting .org/.com to US put Leeds and
# Codeando Mexico in the United States, so those now need a second signal.
US_TLD = ("gov", "us")
AMBIGUOUS_TLD = ("org", "com", "net", "info", "eu")

ISO2 = {"GB": "United Kingdom", "US": "United States", "BR": "Brazil", "IT": "Italy",
        "ES": "Spain", "CA": "Canada", "DE": "Germany", "AR": "Argentina",
        "CL": "Chile", "MX": "Mexico", "AU": "Australia", "CH": "Switzerland",
        "NL": "Netherlands", "DK": "Denmark", "FR": "France", "AT": "Austria"}

# Where the derivation has no chance: portals whose name or country cannot be
# read off the domain or a title. Listed rather than hidden.
OVERRIDES = {
    "dati.retecivica.bz.it": ("Bolzano", "Italy"),
    "datos.codeandomexico.org": ("Codeando México (civic org)", "Mexico"),
    "leedsdatamill.org": ("Leeds", "United Kingdom"),
    "datosabiertos.malaga.eu": ("Málaga", "Spain"),
    "data.qld.gov.au": ("Queensland (state)", "Australia"),
    "portal.opendata.dk": ("Denmark (multi-city)", "Denmark"),
    "data.nantou.gov.tw": ("Nantou", "Taiwan"),
    "donnees.ville.montreal.qc.ca": ("Montréal", "Canada"),
    "data.stadt-zuerich.ch": ("Zürich", "Switzerland"),
    "dados.pbh.gov.br": ("Belo Horizonte", "Brazil"),
    "dados.prefeitura.sp.gov.br": ("São Paulo", "Brazil"),
    "data.buenosaires.gob.ar": ("Buenos Aires", "Argentina"),
    "datos.ciudaddemendoza.gob.ar": ("Mendoza", "Argentina"),
    "datos.ciudaddemendoza.gov.ar": ("Mendoza", "Argentina"),
    "www.datos.misiones.gov.ar": ("Misiones (province)", "Argentina"),
    "datosabiertos.rivasciudad.es": ("Rivas-Vaciamadrid", "Spain"),
    "data.brla.gov": ("Baton Rouge", "United States"),
    "data.kcmo.org": ("Kansas City", "United States"),
    "data.nola.gov": ("New Orleans", "United States"),
    "data.sustainablesm.org": ("Santa Monica", "United States"),
    "www.transparentrichmond.org": ("Richmond, CA", "United States"),
    "data.richmondgov.com": ("Richmond, VA", "United States"),
    "performance.cityofrc.us": ("Rancho Cordova", "United States"),
    "www.opendata-hro.de": ("Rostock", "Germany"),
    "dati.lazio.it": ("Lazio (region)", "Italy"),
    "data.zagreb.hr": ("Zagreb", "Croatia"),
    "transparenz.karlsruhe.de": ("Karlsruhe", "Germany"),
    "dati.comune.matera.it": ("Matera", "Italy"),
    "data.lacity.org": ("Los Angeles", "United States"),
    "controllerdata.lacity.org": ("Los Angeles (Controller)", "United States"),
    "cityofcamas.demo.socrata.com": ("Camas", "United States"),
    "performance.cityofcamas.us": ("Camas", "United States"),
    "cityoffairfaxpd.data.socrata.com": ("Fairfax (police)", "United States"),
    "gainesville-govstat.demo.socrata.com": ("Gainesville", "United States"),
    "janesville.data.socrata.com": ("Janesville", "United States"),
    "kirklandwa.data.socrata.com": ("Kirkland", "United States"),
    "openperformance.edmonton.ca": ("Edmonton", "Canada"),
    "data.calgary.ca": ("Calgary", "Canada"),
    "data.winnipeg.ca": ("Winnipeg", "Canada"),
    "dados.recife.pe.gov.br": ("Recife", "Brazil"),
    "dados.fortaleza.ce.gov.br": ("Fortaleza", "Brazil"),
}

PREFIX = ("data", "datos", "dados", "dati", "opendata", "open", "portal", "datahub",
          "citydata", "performance", "transparent", "transparenz", "fiscalfocus",
          "covid19", "controllerdata", "openperformance", "my", "www", "cos",
          "donnees", "ville", "datosabiertos", "catalogodatos")
DROP = ("gov", "org", "com", "net", "us", "info", "data", "opendata", "socrata",
        "demo", "city", "cityof", "ciudad", "comune", "prefeitura", "stadt",
        "retecivica", "datamill", "qc", "ce", "pe", "sp", "mg", "rs", "wa", "ma",
        "oh", "ca", "ri", "wi", "az", "tx", "il", "pa", "va", "ny", "mo", "mi",
        "hro", "az", "nl")


def country_for(host, existing="", acs_matched=False):
    tld = host.rsplit(".", 1)[-1].lower()
    if tld in TLD_COUNTRY:
        return TLD_COUNTRY[tld], "tld"
    if tld in US_TLD:
        return "United States", "tld"
    if existing and existing.upper() in ISO2:
        return ISO2[existing.upper()], "ckan-registry"
    if tld in AMBIGUOUS_TLD and acs_matched:
        return "United States", "acs"          # an ACS place match proves US
    return "", "unresolved"


def city_from_domain(host):
    parts = [p for p in re.split(r"[.\-_]", host.lower()) if p]
    words = []
    for p in parts:
        if p in PREFIX or p in DROP or p.isdigit() or len(p) < 3:
            continue
        # split concatenations like cityofnewyork / sanjoseca / mesaaz
        for pre in ("cityof", "ciudadde", "comunedi", "prefeitura", "city"):
            if p.startswith(pre) and len(p) > len(pre) + 2:
                p = p[len(pre):]
        words.append(p)
    return words[0].title() if words else ""


def main():
    inv = json.loads(INV.read_text())
    rows = inv["rows"]
    den = json.loads((ROOT / "cities/denominators.json").read_text())
    acs = {r["portal"]: r.get("city") for r in den["ready"] if r.get("city")}
    reg = {c["domain"].replace("https://", "").replace("http://", "").rstrip("/"): c["name"]
           for c in json.loads((ROOT / "cities/registry.json").read_text())["cities"]}

    for r in rows:
        if r["level"] not in ("city", "city-or-region") or not r.get("datasets"):
            continue
        host = r["portal"]
        if host in OVERRIDES:
            r["city"], r["country_name"] = OVERRIDES[host]
            r["city_source"] = r["country_source"] = "override"
            continue
        if host in acs:
            r["city"], r["city_source"] = acs[host], "acs"
        elif host in reg:
            r["city"], r["city_source"] = reg[host], "registry"
        elif r.get("title"):
            t = re.sub(r"\b(open ?data|data|portal|catalog|dados abertos|datos abiertos|"
                       r"official|government|city of|comune di)\b", "", r["title"], flags=re.I)
            t = re.sub(r"[^\w\s\-áéíóúàèìòùâêôãõçñäöüß]", " ", t).strip(" -·|")
            r["city"], r["city_source"] = (t.split()[0].title() if t.split() else
                                           city_from_domain(host)), "title"
        else:
            r["city"], r["city_source"] = city_from_domain(host), "domain"
        c, src = country_for(host, r.get("country", ""), acs_matched=host in acs)
        r["country_name"], r["country_source"] = c, src

    INV.write_text(json.dumps(inv, indent=1))
    done = [r for r in rows if r.get("city")]
    print(f"identified {len(done)} municipal portals")
    import collections
    print("city name source:", dict(collections.Counter(r["city_source"] for r in done)))
    print("country source:  ", dict(collections.Counter(r["country_source"] for r in done)))


if __name__ == "__main__":
    main()
