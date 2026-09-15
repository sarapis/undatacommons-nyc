---
layout: default
title: Municipal portals — 2026-09-15
---

# Municipal open data portals — 2026-09-15

**70 city and regional portals**, holding 222,806 datasets. 65 scored for matchable UN indicators; 29 have a population denominator wired.

Three gates decide whether a city can produce a chart: a reachable portal, indicators the matcher can find, and a denominator. This table shows all three.

> **≥0.55 is review volume, not quality.** It counts UN indicators whose best match in that catalog clears a fixed similarity bar. Hand-reading candidate lists puts precision near half, and under [spec v0.1](../spec/) a grade is a human judgment regardless. NYC — the only city with hand-verified pairs — scores middling, which is the clearest evidence this column does not rank crosswalk success.

> **City and country are derived**, from an ACS place match, the project registry, a CKAN title, the domain, or a hand override where none of those work. The source is recorded per row in `portals/inventory.json` so a wrong one can be traced.

| City | Country | Portal | Plat | Lang | Datasets | Best | ≥0.55 | ≥0.50 | Denominator |
|---|---|---|---|---|---:|---:|---:|---:|---|
| Bolzano | Italy | [dati.retecivica.bz.it](http://dati.retecivica.bz.it/it) | ckan | it | 930 | 0.74 | **19** | 29 | — |
| Madrid | Spain | [datos.madrid.es](https://datos.madrid.es) | ckan | es | 672 | 0.76 | **16** | 20 | own · snapshot |
| Edmonton | Canada | [data.edmonton.ca](https://data.edmonton.ca) | socrata | en | 1,421 | 0.70 | **15** | 17 | — |
| Calgary | Canada | [data.calgary.ca](https://data.calgary.ca) | socrata | en | 416 | 0.77 | **15** | 25 | — |
| Queensland (state) | Australia | [data.qld.gov.au](http://data.qld.gov.au) | ckan | en | 188,847 | 0.73 | **14** | 20 | — |
| Belo Horizonte | Brazil | [dados.pbh.gov.br](https://dados.pbh.gov.br) | ckan | pt | 606 | 0.73 | **9** | 22 | — |
| Providence | United States | [data.providenceri.gov](https://data.providenceri.gov) | socrata | en | 121 | 0.75 | **9** | 12 | ACS |
| New York | United States | [data.cityofnewyork.us](https://data.cityofnewyork.us) | socrata | en | 2,400 | 0.61 | **8** | 25 | ACS |
| Recife | Brazil | [dados.recife.pe.gov.br](https://dados.recife.pe.gov.br) | ckan | pt | 223 | 0.60 | **8** | 15 | — |
| Fortaleza | Brazil | [dados.fortaleza.ce.gov.br](https://dados.fortaleza.ce.gov.br) | ckan | pt | 637 | 0.68 | **7** | 12 | — |
| São Paulo | Brazil | [dados.prefeitura.sp.gov.br](https://dados.prefeitura.sp.gov.br) | ckan | pt | 482 | 0.57 | **7** | 15 | — |
| Denmark (multi-city) | Denmark | [portal.opendata.dk](http://portal.opendata.dk) | ckan | da | 631 | 0.77 | **6** | 16 | — |
| Santa Monica | United States | [data.sustainablesm.org](https://data.sustainablesm.org) | socrata | en | 134 | 0.74 | **6** | 12 | — |
| Zürich | Switzerland | [data.stadt-zuerich.ch](https://data.stadt-zuerich.ch) | ckan | de | 942 | 0.69 | **5** | 16 | — |
| Austin | United States | [datahub.austintexas.gov](https://datahub.austintexas.gov) | socrata | en | 707 | 0.65 | **5** | 16 | ACS |
| Los Angeles | United States | [data.lacity.org](https://data.lacity.org) | socrata | en | 363 | 0.70 | **5** | 16 | — |
| Cambridge | United States | [data.cambridgema.gov](https://data.cambridgema.gov) | socrata | en | 281 | 0.75 | **5** | 18 | ACS |
| Winnipeg | Canada | [data.winnipeg.ca](https://data.winnipeg.ca) | socrata | en | 235 | 0.70 | **5** | 12 | — |
| Milan | Italy | [dati.comune.milano.it](https://dati.comune.milano.it) | ckan | it | 2,602 | 0.68 | **4** | 5 | own · series |
| Seattle | United States | [performance.seattle.gov](https://performance.seattle.gov) | socrata | en | 932 | 0.64 | **4** | 6 | ACS |
| Boston | United States | [data.boston.gov](https://data.boston.gov) | ckan | en | 235 | 0.69 | **4** | 6 | ACS |
| Kansas City | United States | [data.kcmo.org](https://data.kcmo.org) | socrata | en | 202 | 0.70 | **4** | 10 | — |
| Richmond, CA | United States | [www.transparentrichmond.org](https://www.transparentrichmond.org) | socrata | en | 141 | 0.60 | **4** | 9 | — |
| Mesa | United States | [citydata.mesaaz.gov](https://citydata.mesaaz.gov) | socrata | en | 303 | 0.59 | **3** | 10 | ACS |
| San Jose | United States | [data.sanjoseca.gov](https://data.sanjoseca.gov) | ckan | en | 170 | 0.65 | **3** | 6 | ACS |
| Karlsruhe | Germany | [transparenz.karlsruhe.de](https://transparenz.karlsruhe.de) | ckan | de | 151 | 0.67 | **3** | 7 | — |
| Everett | United States | [data.everettwa.gov](https://data.everettwa.gov) | socrata | en | 121 | 0.92 | **3** | 4 | ACS |
| Gainesville | United States | [data.cityofgainesville.org](https://data.cityofgainesville.org) | socrata | en | 89 | 0.69 | **3** | 6 | ACS |
| Berkeley | United States | [data.cityofberkeley.info](https://data.cityofberkeley.info) | socrata | en | 44 | 0.62 | **3** | 7 | ACS |
| Oakland | United States | [data.oaklandca.gov](https://data.oaklandca.gov) | socrata | en | 313 | 0.68 | **2** | 2 | ACS |
| Matera | Italy | [dati.comune.matera.it](https://dati.comune.matera.it) | ckan | it | 249 | 0.65 | **2** | 5 | — |
| Baton Rouge | United States | [data.brla.gov](https://data.brla.gov) | socrata | en | 239 | 0.82 | **2** | 6 | — |
| New Orleans | United States | [data.nola.gov](https://data.nola.gov) | socrata | en | 209 | 0.68 | **2** | 3 | — |
| Mendoza | Argentina | [datos.ciudaddemendoza.gob.ar](http://datos.ciudaddemendoza.gob.ar) | ckan | es | 180 | 0.70 | **2** | 3 | — |
| Mendoza | Argentina | [datos.ciudaddemendoza.gov.ar](http://datos.ciudaddemendoza.gov.ar) | ckan | es | 180 | 0.70 | **2** | 3 | — |
| Norfolk | United States | [data.norfolk.gov](https://data.norfolk.gov) | socrata | en | 103 | 0.66 | **2** | 8 | ACS |
| Roseville | United States | [data.roseville.ca.us](https://data.roseville.ca.us) | socrata | en | 60 | 0.65 | **2** | 4 | ACS |
| Edmonton | Canada | [openperformance.edmonton.ca](https://openperformance.edmonton.ca) | socrata | en | 9 | 0.71 | **2** | 2 | — |
| Chicago | United States | [data.cityofchicago.org](https://data.cityofchicago.org) | socrata | en | 915 | 0.61 | **1** | 6 | ACS |
| Nantou | Taiwan | [data.nantou.gov.tw](http://data.nantou.gov.tw) | ckan | en | 430 | 0.58 | **1** | 1 | — |
| Seattle | United States | [cos-data.seattle.gov](https://cos-data.seattle.gov) | socrata | en | 147 | 0.58 | **1** | 1 | ACS |
| Janesville | United States | [performance.ci.janesville.wi.us](https://performance.ci.janesville.wi.us) | socrata | en | 73 | 0.56 | **1** | 5 | ACS |
| Gainesville | United States | [gainesville-govstat.demo.socrata.com](https://gainesville-govstat.demo.socrata.com) | socrata | en | 68 | 0.61 | **1** | 1 | ACS |
| Orlando | United States | [data.cityoforlando.net](https://data.cityoforlando.net) | socrata | en | 27 | 0.59 | **1** | 3 | ACS |
| Codeando México (civic org) | Mexico | [datos.codeandomexico.org](http://datos.codeandomexico.org) | ckan | en | 9,761 | 0.44 | **0** | 0 | — |
| Málaga | Spain | [datosabiertos.malaga.eu](http://datosabiertos.malaga.eu) | ckan | en | 1,377 | 0.35 | **0** | 0 | — |
| Montréal | Canada | [donnees.ville.montreal.qc.ca](https://donnees.ville.montreal.qc.ca) | ckan | en | 404 | 0.38 | **0** | 0 | — |
| Dallas | United States | [www.dallasopendata.com](https://www.dallasopendata.com) | socrata | en | 342 | 0.53 | **0** | 2 | ACS |
| Zagreb | Croatia | [data.zagreb.hr](https://data.zagreb.hr) | ckan | hr | 199 | 0.45 | **0** | 0 | — |
| Cincinnati | United States | [data.cincinnati-oh.gov](https://data.cincinnati-oh.gov) | socrata | en | 102 | 0.46 | **0** | 0 | ACS |
| Los Angeles (Controller) | United States | [controllerdata.lacity.org](https://controllerdata.lacity.org) | socrata | en | 87 | 0.53 | **0** | 2 | — |
| Camas | United States | [performance.cityofcamas.us](https://performance.cityofcamas.us) | socrata | en | 64 | 0.54 | **0** | 1 | — |
| Janesville | United States | [janesville.data.socrata.com](https://janesville.data.socrata.com) | socrata | en | 42 | 0.47 | **0** | 0 | ACS |
| Rancho Cordova | United States | [performance.cityofrc.us](https://performance.cityofrc.us) | socrata | en | 35 | 0.49 | **0** | 0 | — |
| Somerville | United States | [data.somervillema.gov](https://data.somervillema.gov) | socrata | en | 33 | 0.47 | **0** | 0 | ACS |
| Richmond, VA | United States | [data.richmondgov.com](https://data.richmondgov.com) | socrata | en | 31 | 0.41 | **0** | 0 | — |
| Buffalony | United States | [covid19.buffalony.gov](https://covid19.buffalony.gov) | socrata | en | 21 | 0.40 | **0** | 0 | — |
| Mesa | United States | [data.mesaaz.gov](https://data.mesaaz.gov) | socrata | en | 18 | 0.51 | **0** | 1 | ACS |
| Pittsburgh | United States | [fiscalfocus.pittsburghpa.gov](https://fiscalfocus.pittsburghpa.gov) | socrata | en | 15 | 0.44 | **0** | 0 | ACS |
| Camas | United States | [cityofcamas.demo.socrata.com](https://cityofcamas.demo.socrata.com) | socrata | en | 8 | 0.52 | **0** | 1 | — |
| Rivas-Vaciamadrid | Spain | [datosabiertos.rivasciudad.es](http://datosabiertos.rivasciudad.es) | ckan | es | 7 | 0.47 | **0** | 0 | — |
| Fairfax (police) | United States | [cityoffairfaxpd.data.socrata.com](https://cityoffairfaxpd.data.socrata.com) | socrata | en | 6 | 0.41 | **0** | 0 | — |
| Mesquite | United States | [opendata.cityofmesquite.com](https://opendata.cityofmesquite.com) | socrata | en | 4 | 0.45 | **0** | 0 | ACS |
| Kirkland | United States | [kirklandwa.data.socrata.com](https://kirklandwa.data.socrata.com) | socrata | en | 2 | 0.41 | **0** | 0 | ACS |
| Misiones (province) | Argentina | [www.datos.misiones.gov.ar](http://www.datos.misiones.gov.ar) | ckan | es | 2 | 0.32 | **0** | 0 | — |
| Leeds | United Kingdom | [leedsdatamill.org](https://leedsdatamill.org) | ckan | ? | 641 | — | — | — | — |
| Buenos Aires | Argentina | [data.buenosaires.gob.ar](https://data.buenosaires.gob.ar) | ckan | es | 454 | — | — | — | — |
| Lazio (region) | Italy | [dati.lazio.it](http://dati.lazio.it) | ckan | ? | 406 | — | — | — | — |
| Rostock | Germany | [www.opendata-hro.de](https://www.opendata-hro.de) | ckan | ? | 282 | — | — | — | — |
| Recife | Brazil | [dados.recife.pe.gov.br](https://dados.recife.pe.gov.br) | ckan | ? | 223 | — | — | — | — |

## Reading it

- **Catalog size does not predict potential.** Bolzano has 930 datasets and 19 indicators above 0.55; Milan has 2,602 and 4.
- **Four of the top six are non-English**, and returned zero candidates before a multilingual embedding model was added.
- **The denominator is the binding gate.** Most SDG indicators are rates per 100,000, so a city with 19 candidates and no population source still cannot chart one. 27 US cities resolve via Census ACS; Madrid and Milan are wired from their own statistical publications; the rest need one.
