---
layout: default
title: UN graph smell test — 2026-09-16
---

# UN graph smell test — 2026-09-16

Plausibility checks run against the UN System Data Commons from outside it. The checks are deliberately dumb — a percentage above 100, a negative count, a rate exceeding its own denominator, one value repeated across countries that should not agree. None of them require subject-matter knowledge, which is why an outsider can run them at all.

**This flags; it does not judge.** A gross enrolment ratio above 100% is *correct*. A flatline can be a country that genuinely did not change. Every row below is a question for someone who knows the indicator, not a defect report. The indicator name is printed against every row so that person can answer it.

**Scope:** the 442 indicators screened usable (GREEN/AMBER/RANK-ONLY) — **442 indicators**, **768,279 observations** across every reporting country and year.

**2,457 findings** across 8 checks.

### What the checks reach

Range checks depend on knowing what the unit means. Most of the corpus is percentages and counts; the rest gets only the unit-agnostic checks (jump, flatline, shared value, future date). This table is here so the headline count is read against what was actually inspected.

| Unit kind | Indicators | Observations | Range checks |
|---|---:|---:|---|
| percent | 222 | 364,461 | yes — 0–100 |
| other | 123 | 248,457 | **no** — unit-agnostic checks only |
| count | 76 | 114,302 | yes — non-negative |
| scaled | 21 | 41,059 | yes — capped by denominator |

| Check | Severity | Findings | Indicators | What it means |
|---|---|---:|---:|---|
| `outlier` | HIGH | 50 | 16 | At least 20x the indicator's own 99th percentile across every country and year. Scale-free, so it survives when an absolute range check has been suppressed as structural — and it is the only check that reaches units with no meaningful range. |
| `percent_negative` | HIGH | 38 | 11 | A percentage below zero is not a measurement. |
| `rate_over_scale` | HIGH | 4 | 1 | The rate exceeds its own denominator. Written expecting 'more events than there are people to have them' — but all four hits are disaster-affected persons per 100,000, where a person counts once per disaster, so exceeding the population is correct for a country hit repeatedly in one year. The check stands because the same shape on a rate that cannot repeat would be a real error; the premise, as written, was wrong. |
| `jump` | MEDIUM | 523 | 92 | Changed by a factor of 10+ in one year, by a margin worth 5%+ of the series' own range. A real shock, a revision, or a units change. Only run on non-negative counts, rates and percentages — a ratio means nothing on a signed index. |
| `percent_over_100` | MEDIUM | 205 | 18 | Above 100%. Sometimes correct — gross enrolment ratios count pupils outside the nominal age band in the numerator only, and Kuwait's water stress genuinely exceeds its renewable resources — and sometimes it is Malaysia recycling 147.7% of its municipal waste. Needs a human. |
| `shared_value` | MEDIUM | 175 | 10 | An identical value carrying 3+ decimals, in 5+ countries for the same year. Countries do not agree to that precision by chance; this is the shape of a modelled default. |
| `flatline` | LOW | 803 | 76 | 6+ consecutive identical non-zero values. Either nothing changed, or a figure is being carried forward. |
| `flatline_zero` | LOW | 659 | 82 | 10+ consecutive zeros. Often true of small states; occasionally a missing value written as 0. |

## `outlier` — HIGH · 50 findings

At least 20x the indicator's own 99th percentile across every country and year. Scale-free, so it survives when an absolute range check has been suppressed as structural — and it is the only check that reaches units with no meaningful range.

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Electronic waste collected per capita | Guadeloupe | 2022 | 13951.2 | `WEIGHT_KG` | 110x the indicator's p99 (127.2); median 6.56 |
| Hazardous waste exported | Australia | 2007 | 3.83761e+07 | `WEIGHT_TN` | 23x the indicator's p99 (1.647e+06); median 9,557 |
| Hazardous waste exported | Canada | 2007 | 4.52398e+08 | `WEIGHT_TN` | 275x the indicator's p99 (1.647e+06); median 9,557 |
| Hazardous waste exported | Japan | 2007 | 4.9e+07 | `WEIGHT_TN` | 30x the indicator's p99 (1.647e+06); median 9,557 |
| Hazardous waste exported | Mexico | 2007 | 1.51365e+08 | `WEIGHT_TN` | 92x the indicator's p99 (1.647e+06); median 9,557 |
| Hazardous waste generated, per capita | Brunei | 2016 | 1.25754e+07 | `WEIGHT_KG` | 111x the indicator's p99 (1.135e+05); median 22.61 |
| Hazardous waste generated, per capita | Brunei | 2017 | 3.60643e+07 | `WEIGHT_KG` | 318x the indicator's p99 (1.135e+05); median 22.61 |
| Hazardous waste generated, per capita | Brunei | 2018 | 8.7562e+06 | `WEIGHT_KG` | 77x the indicator's p99 (1.135e+05); median 22.61 |
| Hazardous waste generated, per capita | Brunei | 2019 | 8.68e+06 | `WEIGHT_KG` | 76x the indicator's p99 (1.135e+05); median 22.61 |
| Hazardous waste generated, per capita | Brunei | 2020 | 1.17738e+07 | `WEIGHT_KG` | 104x the indicator's p99 (1.135e+05); median 22.61 |
| Hazardous waste generated, per capita | Brunei | 2021 | 1.36885e+07 | `WEIGHT_KG` | 121x the indicator's p99 (1.135e+05); median 22.61 |
| Hazardous waste generated, per capita | Brunei | 2022 | 1.89737e+07 | `WEIGHT_KG` | 167x the indicator's p99 (1.135e+05); median 22.61 |
| Hazardous waste generated, per capita | Brunei | 2023 | 2.08613e+07 | `WEIGHT_KG` | 184x the indicator's p99 (1.135e+05); median 22.61 |
| Proportion of hazardous waste that is treated or disposed | Guatemala | 2011 | 33022.7 | `Percent` | 57x the indicator's p99 (574.8); median 87.94 |
| Proportion of hazardous waste that is treated or disposed | Guatemala | 2012 | 44825.7 | `Percent` | 78x the indicator's p99 (574.8); median 87.94 |
| Beach litter items per unit of surface area (Number of items per | Saudi Arabia | 2015 | 9.36e+06 | `RATIO_COUNT_PER_100_AREA_M2` | 375x the indicator's p99 (2.497e+04); median 68 |
| Municipal waste recycled | South Africa | 2018 | 1.85531e+09 | `WEIGHT_TN` | 32x the indicator's p99 (5.724e+07); median 4.56e+05 |
| Municipal waste recycled | South Africa | 2019 | 3.44268e+09 | `WEIGHT_TN` | 60x the indicator's p99 (5.724e+07); median 4.56e+05 |
| Municipal waste recycled | South Africa | 2021 | 2.21792e+09 | `WEIGHT_TN` | 39x the indicator's p99 (5.724e+07); median 4.56e+05 |
| Municipal waste recycled | South Africa | 2022 | 1.46408e+09 | `WEIGHT_TN` | 26x the indicator's p99 (5.724e+07); median 4.56e+05 |
| Municipal waste recycled | South Africa | 2023 | 1.32913e+09 | `WEIGHT_TN` | 23x the indicator's p99 (5.724e+07); median 4.56e+05 |
| Ratio of non-performing loans (net of provisions) to capital | Equatorial Guinea | 2022 | 10133.9 | `Percent` | 48x the indicator's p99 (210.7); median 9.138 |
| Ratio of broad money to total reserves | Sierra Leone | 2001 | 2801.8 | `RATIO` | 54x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2002 | 2073.49 | `RATIO` | 40x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2003 | 2875.55 | `RATIO` | 56x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2004 | 1599.11 | `RATIO` | 31x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2005 | 1438.47 | `RATIO` | 28x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2006 | 1582.73 | `RATIO` | 31x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2007 | 1561.99 | `RATIO` | 30x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2008 | 1946.48 | `RATIO` | 38x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2009 | 1253.72 | `RATIO` | 24x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2010 | 1311.76 | `RATIO` | 25x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2011 | 1448.51 | `RATIO` | 28x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2012 | 1625.24 | `RATIO` | 32x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2013 | 1618.8 | `RATIO` | 31x the indicator's p99 (51.47); median 2.995 |
| Ratio of broad money to total reserves | Sierra Leone | 2014 | 1702.75 | `RATIO` | 33x the indicator's p99 (51.47); median 2.995 |
| Annual growth of broad money | Sierra Leone | 2001 | 131119 | `Percent` | 1,573x the indicator's p99 (83.38); median 11.19 |
| Alternative conversion factor used by the Development Economics  | Iran | 2023 | 353510 | `RATIO` | 22x the indicator's p99 (1.63e+04); median 6.732 |
| Alternative conversion factor used by the Development Economics  | Iran | 2024 | 452865 | `RATIO` | 28x the indicator's p99 (1.63e+04); median 6.732 |
| Number of injured or ill people attributed to disasters | India | 2018 | 1.41608e+08 | `COUNT` | 68x the indicator's p99 (2.078e+06); median 96 |
| Number of deaths and missing persons attributed to disasters | country/USA | 2020 | 345950 | `COUNT` | 27x the indicator's p99 (1.275e+04); median 44 |
| Number of deaths and missing persons attributed to disasters | country/USA | 2021 | 470644 | `COUNT` | 37x the indicator's p99 (1.275e+04); median 44 |
| Number of deaths due to disaster | United States | 2020 | 345950 | `COUNT` | 27x the indicator's p99 (1.275e+04); median 42 |
| Number of deaths due to disaster | United States | 2021 | 470644 | `COUNT` | 37x the indicator's p99 (1.275e+04); median 42 |
| Number of deaths and missing persons attributed to disasters per | Haiti | 2010 | 2276.54 | `RATIO_COUNT_PER_100000_COUNT_POP` | 20x the indicator's p99 (113.6); median 0.327 |
| Number of people whose damaged dwellings were attributed to disa | India | 2015 | 1.87873e+08 | `COUNT` | 75x the indicator's p99 (2.491e+06); median 3,008 |
| Number of people whose damaged dwellings were attributed to disa | India | 2016 | 1.76836e+08 | `COUNT` | 71x the indicator's p99 (2.491e+06); median 3,008 |
| Number of people whose damaged dwellings were attributed to disa | India | 2017 | 1.74547e+08 | `COUNT` | 70x the indicator's p99 (2.491e+06); median 3,008 |
| Number of people whose damaged dwellings were attributed to disa | India | 2019 | 5.33247e+07 | `COUNT` | 21x the indicator's p99 (2.491e+06); median 3,008 |
| Detected victims of human trafficking for removal of organ | Malaysia | 2016 | 676 | `COUNT` | 26x the indicator's p99 (26); median 0 |

## `percent_negative` — HIGH · 38 findings

A percentage below zero is not a measurement.

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Net outbound official development assistance (ODA) to LDCs as a  | Kuwait | 2018 | -0.430694 | `Percent` |  |
| Net outbound official development assistance (ODA) to LDCs as a  | Thailand | 2010 | -0.001692 | `Percent` |  |
| Net outbound official development assistance (ODA) to landlocked | Kuwait | 2019 | -0.0012 | `Percent` |  |
| Sustainable fisheries as a proportion of GDP | Malta | 2023 | -0.01 | `Percent` |  |
| Fossil-fuel subsidies (consumption and production) as a proporti | Peru | 2015 | -0.07842 | `Percent` |  |
| Fossil-fuel subsidies (consumption and production) as a proporti | Peru | 2016 | -0.06377 | `Percent` |  |
| Fossil-fuel subsidies (consumption and production) as a proporti | Peru | 2017 | -0.05916 | `Percent` |  |
| Fossil-fuel subsidies (consumption and production) as a proporti | Peru | 2018 | -0.06329 | `Percent` |  |
| Fossil-fuel subsidies (consumption and production) as a proporti | Peru | 2021 | -0.05636 | `Percent` |  |
| Fossil-fuel subsidies (consumption and production) as a proporti | Peru | 2022 | -0.31737 | `Percent` |  |
| Fossil-fuel subsidies (consumption and production) as a proporti | Peru | 2023 | -0.07154 | `Percent` |  |
| Bank capital to assets ratio | Equatorial Guinea | 2019 | -0.706329 | `Percent` |  |
| Bank capital to assets ratio | Equatorial Guinea | 2020 | -0.170105 | `Percent` |  |
| Bank capital to assets ratio | Equatorial Guinea | 2021 | -1.32253 | `Percent` |  |
| Bank capital to assets ratio | Equatorial Guinea | 2023 | -6.40253 | `Percent` |  |
| Bank capital to assets ratio | Greece | 2011 | -1.26152 | `Percent` |  |
| Bank capital to assets ratio | Chad | 2023 | -1.04363 | `Percent` |  |
| Ratio of regulatory capital to assets | Anguilla | 2015 | -2.85217 | `Percent` |  |
| Ratio of regulatory capital to assets | Equatorial Guinea | 2019 | -0.706329 | `Percent` |  |
| Ratio of regulatory capital to assets | Equatorial Guinea | 2020 | -0.170105 | `Percent` |  |
| Ratio of regulatory capital to assets | Equatorial Guinea | 2021 | -1.32253 | `Percent` |  |
| Ratio of regulatory capital to assets | Equatorial Guinea | 2023 | -6.40253 | `Percent` |  |
| Ratio of regulatory capital to assets | Greece | 2011 | -1.26152 | `Percent` |  |
| Ratio of regulatory capital to assets | Chad | 2023 | -1.04363 | `Percent` |  |
| Ratio of regulatory tier-1 capital to risk-weighted assets | Anguilla | 2015 | -5.01916 | `Percent` |  |
| Ratio of regulatory tier-1 capital to risk-weighted assets | Equatorial Guinea | 2019 | -1.60593 | `Percent` |  |
| Ratio of regulatory tier-1 capital to risk-weighted assets | Equatorial Guinea | 2020 | -0.402557 | `Percent` |  |
| Ratio of regulatory tier-1 capital to risk-weighted assets | Equatorial Guinea | 2021 | -4.96672 | `Percent` |  |
| Ratio of regulatory tier-1 capital to risk-weighted assets | Equatorial Guinea | 2023 | -17.5032 | `Percent` |  |
| Ratio of regulatory tier-1 capital to risk-weighted assets | Greece | 2011 | -2.62288 | `Percent` |  |
| Ratio of regulatory tier-1 capital to risk-weighted assets | Chad | 2023 | -1.62065 | `Percent` |  |
| Primary government expenditures as a proportion of original appr | Kiribati | 2018 | -7.54 | `Percent` |  |
| Primary government expenditures as a proportion of original appr | Kiribati | 2020 | -17.875 | `Percent` |  |
| Average remittance costs of sending $200 to a receiving country  | Myanmar | 2022 | -0.56 | `Percent` |  |
| Average remittance costs of sending $200 to a receiving country  | Malawi | 2023 | -0.1 | `Percent` |  |
| Average remittance costs of sending $200 to a receiving country  | Malawi | 2024 | -0.93 | `Percent` |  |
| Average remittance costs of sending $200 for a sending country a | Ghana | 2022 | -4.04 | `Percent` |  |
| Tourism direct GDP as a proportion of total GDP | Fiji | 2021 | -0.1 | `Percent` |  |

## `rate_over_scale` — HIGH · 4 findings

The rate exceeds its own denominator. Written expecting 'more events than there are people to have them' — but all four hits are disaster-affected persons per 100,000, where a person counts once per disaster, so exceeding the population is correct for a country hit repeatedly in one year. The check stands because the same shape on a rate that cannot repeat would be a real error; the premise, as written, was wrong.

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Number of directly affected persons attributed to disasters per  | Barbados | 2021 | 105025 | `RATIO_COUNT_PER_100000_COUNT_POP` | cap 100,000 |
| Number of directly affected persons attributed to disasters per  | Marshall Islands | 2020 | 132810 | `RATIO_COUNT_PER_100000_COUNT_POP` | cap 100,000 |
| Number of directly affected persons attributed to disasters per  | Marshall Islands | 2022 | 132031 | `RATIO_COUNT_PER_100000_COUNT_POP` | cap 100,000 |
| Number of directly affected persons attributed to disasters per  | Palau | 2021 | 112467 | `RATIO_COUNT_PER_100000_COUNT_POP` | cap 100,000 |

## `jump` — MEDIUM · 523 findings

Changed by a factor of 10+ in one year, by a margin worth 5%+ of the series' own range. A real shock, a revision, or a units change. Only run on non-negative counts, rates and percentages — a ratio means nothing on a signed index.

*Showing the first 60 of 523. The full set is in the JSON beside this page.*

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Food waste | Mauritius | 2022 | 177570 | `WEIGHT_TN` | 206.731 (2021) -> 177570 (2022), x858.9 |
| Proportion of agricultural land area that has achieved an accept | Ecuador | 2022 | 1 | `Percent` | 30 (2021) -> 1 (2022), x0.0 |
| Forest area certified under an independently verified certificat | Cambodia | 2024 | 420 | `AREA_HA` | 8320 (2023) -> 420 (2024), x0.1 |
| Forest area certified under an independently verified certificat | Laos | 2016 | 320 | `AREA_HA` | 132700 (2015) -> 320 (2016), x0.0 |
| Forest area certified under an independently verified certificat | Laos | 2017 | 13550 | `AREA_HA` | 320 (2016) -> 13550 (2017), x42.3 |
| Agriculture value added share of GDP | Malta | 2023 | 0.04 | `Percent` | 0.77 (2022) -> 0.04 (2023), x0.1 |
| Agriculture value added share of GDP | Malta | 2024 | 0.49 | `Percent` | 0.04 (2023) -> 0.49 (2024), x12.2 |
| Agriculture share of Government Expenditure | Guinea | 2021 | 0.29 | `Percent` | 3.61 (2020) -> 0.29 (2021), x0.1 |
| Agriculture share of Government Expenditure | Iran | 2019 | 0.81 | `Percent` | 9.78 (2018) -> 0.81 (2019), x0.1 |
| Agriculture share of Government Expenditure | Pakistan | 2006 | 3.32 | `Percent` | 0.28 (2005) -> 3.32 (2006), x11.9 |
| Agriculture share of Government Expenditure | Saudi Arabia | 2019 | 0.07 | `Percent` | 0.94 (2018) -> 0.07 (2019), x0.1 |
| Agriculture share of Government Expenditure | Sierra Leone | 2014 | 0.12 | `Percent` | 1.55 (2013) -> 0.12 (2014), x0.1 |
| Agriculture share of Government Expenditure | Sierra Leone | 2015 | 2.55 | `Percent` | 0.12 (2014) -> 2.55 (2015), x21.2 |
| Volume of remittances as a proportion of total GDP | Aruba | 2013 | 2.1316 | `Percent` | 0.185849 (2012) -> 2.1316 (2013), x11.5 |
| Volume of remittances as a proportion of total GDP | Angola | 2009 | 0.000230927 | `Percent` | 0.0927098 (2008) -> 0.000230927 (2009), x0.0 |
| Volume of remittances as a proportion of total GDP | Angola | 2010 | 0.0214465 | `Percent` | 0.000230927 (2009) -> 0.0214465 (2010), x92.9 |
| Volume of remittances as a proportion of total GDP | Angola | 2011 | 0.000183157 | `Percent` | 0.0214465 (2010) -> 0.000183157 (2011), x0.0 |
| Volume of remittances as a proportion of total GDP | Angola | 2012 | 0.0315095 | `Percent` | 0.000183157 (2011) -> 0.0315095 (2012), x172.0 |
| Volume of remittances as a proportion of total GDP | Bulgaria | 2001 | 5.8251 | `Percent` | 0.439646 (2000) -> 5.8251 (2001), x13.2 |
| Volume of remittances as a proportion of total GDP | Congo [DRC] | 2011 | 4.36343 | `Percent` | 0.0728007 (2010) -> 4.36343 (2011), x59.9 |
| Volume of remittances as a proportion of total GDP | Congo [Republic] | 2002 | 0.0387737 | `Percent` | 0.433346 (2001) -> 0.0387737 (2002), x0.1 |
| Volume of remittances as a proportion of total GDP | Algeria | 2005 | 0.158809 | `Percent` | 2.67642 (2004) -> 0.158809 (2005), x0.1 |
| Volume of remittances as a proportion of total GDP | Algeria | 2014 | 1.02637 | `Percent` | 0.0912495 (2013) -> 1.02637 (2014), x11.2 |
| Volume of remittances as a proportion of total GDP | Ghana | 2011 | 5.42659 | `Percent` | 0.421932 (2010) -> 5.42659 (2011), x12.9 |
| Volume of remittances as a proportion of total GDP | Guinea | 2021 | 2.01481 | `Percent` | 0.159915 (2020) -> 2.01481 (2021), x12.6 |
| Volume of remittances as a proportion of total GDP | Iraq | 2007 | 0.00348953 | `Percent` | 0.596957 (2006) -> 0.00348953 (2007), x0.0 |
| Volume of remittances as a proportion of total GDP | Kenya | 2001 | 0.392071 | `Percent` | 4.23365 (2000) -> 0.392071 (2001), x0.1 |
| Volume of remittances as a proportion of total GDP | Kuwait | 2015 | 0.0299042 | `Percent` | 0.00236059 (2014) -> 0.0299042 (2015), x12.7 |
| Volume of remittances as a proportion of total GDP | Kuwait | 2021 | 0.543351 | `Percent` | 0.0202777 (2020) -> 0.543351 (2021), x26.8 |
| Volume of remittances as a proportion of total GDP | Kuwait | 2022 | 0.0120152 | `Percent` | 0.543351 (2021) -> 0.0120152 (2022), x0.0 |
| Volume of remittances as a proportion of total GDP | Liberia | 2010 | 14.7263 | `Percent` | 1.42064 (2009) -> 14.7263 (2010), x10.4 |
| Volume of remittances as a proportion of total GDP | Malta | 2004 | 5.22956 | `Percent` | 0.476067 (2003) -> 5.22956 (2004), x11.0 |
| Volume of remittances as a proportion of total GDP | Malta | 2017 | 0.171301 | `Percent` | 2.09075 (2016) -> 0.171301 (2017), x0.1 |
| Volume of remittances as a proportion of total GDP | Mongolia | 2001 | 2.10448 | `Percent` | 0.0968694 (2000) -> 2.10448 (2001), x21.7 |
| Volume of remittances as a proportion of total GDP | Mauritania | 2021 | 0.142859 | `Percent` | 2.04177 (2020) -> 0.142859 (2021), x0.1 |
| Volume of remittances as a proportion of total GDP | Mauritius | 2001 | 0.0131712 | `Percent` | 3.74515 (2000) -> 0.0131712 (2001), x0.0 |
| Volume of remittances as a proportion of total GDP | Mauritius | 2014 | 2.50141 | `Percent` | 0.00449753 (2013) -> 2.50141 (2014), x556.2 |
| Volume of remittances as a proportion of total GDP | Malawi | 2003 | 0.297918 | `Percent` | 0.0165842 (2002) -> 0.297918 (2003), x18.0 |
| Volume of remittances as a proportion of total GDP | Papua New Guinea | 2020 | 0.00963229 | `Percent` | 0.118574 (2019) -> 0.00963229 (2020), x0.1 |
| Volume of remittances as a proportion of total GDP | Sierra Leone | 2005 | 0.0956716 | `Percent` | 1.10465 (2004) -> 0.0956716 (2005), x0.1 |
| Volume of remittances as a proportion of total GDP | country/SSD | 2015 | 9.49107 | `Percent` | 0.0142213 (2014) -> 9.49107 (2015), x667.4 |
| Volume of remittances as a proportion of total GDP | country/SUR | 2002 | 1.38079 | `Percent` | 0.0239728 (2001) -> 1.38079 (2002), x57.6 |
| Volume of remittances as a proportion of total GDP | country/SUR | 2017 | 2.7261 | `Percent` | 0.0450212 (2016) -> 2.7261 (2017), x60.6 |
| Volume of remittances as a proportion of total GDP | country/SVK | 2003 | 0.912396 | `Percent` | 0.0692004 (2002) -> 0.912396 (2003), x13.2 |
| Volume of remittances as a proportion of total GDP | country/URY | 2002 | 0.264969 | `Percent` | 2.88918e-05 (2001) -> 0.264969 (2002), x9171.1 |
| Volume of remittances as a proportion of total GDP | country/VEN | 2003 | 0.248742 | `Percent` | 0.0204535 (2002) -> 0.248742 (2003), x12.2 |
| Volume of remittances as a proportion of total GDP | country/WSM | 2004 | 0.22018 | `Percent` | 13.4962 (2003) -> 0.22018 (2004), x0.0 |
| Volume of remittances as a proportion of total GDP | country/WSM | 2005 | 17.1146 | `Percent` | 0.22018 (2004) -> 17.1146 (2005), x77.7 |
| Amount of tracked imported Environmentally Sound Technologies | Albania | 2022 | 1.89121e+07 | `CR_USD` | 2.37869e+08 (2021) -> 1.89121e+07 (2022), x0.1 |
| Amount of tracked imported Environmentally Sound Technologies | Albania | 2023 | 3.80945e+08 | `CR_USD` | 1.89121e+07 (2022) -> 3.80945e+08 (2023), x20.1 |
| Total trade of tracked Environmentally Sound Technologies | Albania | 2022 | 1.98408e+07 | `CR_USD` | 2.66923e+08 (2021) -> 1.98408e+07 (2022), x0.1 |
| Total trade of tracked Environmentally Sound Technologies | Albania | 2023 | 4.26456e+08 | `CR_USD` | 1.98408e+07 (2022) -> 4.26456e+08 (2023), x21.5 |
| Total trade of tracked Environmentally Sound Technologies | Montserrat | 2011 | 1.6086e+06 | `CR_USD` | 28620 (2010) -> 1.6086e+06 (2011), x56.2 |
| Total trade of tracked Environmentally Sound Technologies | Qatar | 2011 | 8.80714e+06 | `CR_USD` | 2.59087e+09 (2010) -> 8.80714e+06 (2011), x0.0 |
| Total trade of tracked Environmentally Sound Technologies | Qatar | 2012 | 2.08723e+09 | `CR_USD` | 8.80714e+06 (2011) -> 2.08723e+09 (2012), x237.0 |
| Net outbound official development assistance (ODA) as a percenta | Thailand | 2010 | 0.001316 | `Percent` | 0.018729 (2009) -> 0.001316 (2010), x0.1 |
| Net outbound official development assistance (ODA) from OECD-DAC | Kuwait | 2023 | 1.1041e+07 | `CR_USD_K` | 1.9863e+08 (2022) -> 1.1041e+07 (2023), x0.1 |
| Net outbound official development assistance (ODA) from OECD-DAC | Saudi Arabia | 2002 | 3.82116e+09 | `CR_USD_K` | 3.2675e+08 (2001) -> 3.82116e+09 (2002), x11.7 |
| Net outbound official development assistance (ODA) from OECD-DAC | Saudi Arabia | 2015 | 9.89447e+08 | `CR_USD_K` | 1.41918e+10 (2014) -> 9.89447e+08 (2015), x0.1 |
| Debt service as a proportion of exports of goods and services | Belize | 2022 | 5.25143 | `Percent` | 58.4508 (2021) -> 5.25143 (2022), x0.1 |

## `percent_over_100` — MEDIUM · 205 findings

Above 100%. Sometimes correct — gross enrolment ratios count pupils outside the nominal age band in the numerator only, and Kuwait's water stress genuinely exceeds its renewable resources — and sometimes it is Malaysia recycling 147.7% of its municipal waste. Needs a human.

*Showing the first 60 of 205. The full set is in the JSON beside this page.*

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Current account balance as a proportion of GDP | country/TLS | 2006 | 119.207 | `Percent` |  |
| Current account balance as a proportion of GDP | country/TLS | 2007 | 216.878 | `Percent` |  |
| Current account balance as a proportion of GDP | country/TLS | 2008 | 311.746 | `Percent` |  |
| Current account balance as a proportion of GDP | country/TLS | 2009 | 176.763 | `Percent` |  |
| Current account balance as a proportion of GDP | country/TLS | 2010 | 189.518 | `Percent` |  |
| Current account balance as a proportion of GDP | country/TLS | 2011 | 225.033 | `Percent` |  |
| Current account balance as a proportion of GDP | country/TLS | 2012 | 235.751 | `Percent` |  |
| Current account balance as a proportion of GDP | country/TLS | 2013 | 171.239 | `Percent` |  |
| Debt service as a proportion of exports of goods and services | Burundi | 2004 | 134.722 | `Percent` |  |
| Debt service as a proportion of exports of goods and services | Liberia | 2007 | 114.387 | `Percent` |  |
| Debt service as a proportion of exports of goods and services | Liberia | 2008 | 119.68 | `Percent` |  |
| Debt service as a proportion of exports of goods and services | Sierra Leone | 2001 | 112.303 | `Percent` |  |
| Proportion of municipal waste recycled | Malaysia | 2017 | 112.006 | `Percent` |  |
| Proportion of municipal waste recycled | Malaysia | 2018 | 128.663 | `Percent` |  |
| Proportion of municipal waste recycled | Malaysia | 2019 | 147.665 | `Percent` |  |
| Proportion of municipal waste recycled | Malaysia | 2020 | 177.658 | `Percent` |  |
| Change in minimum river flow (%) | Aruba | 2013 | 119.532 | `Percent` |  |
| Change in minimum river flow (%) | Aruba | 2014 | 117.923 | `Percent` |  |
| Change in minimum river flow (%) | Anguilla | 2012 | 142.85 | `Percent` |  |
| Change in minimum river flow (%) | Anguilla | 2013 | 150.815 | `Percent` |  |
| Change in minimum river flow (%) | Anguilla | 2014 | 132.678 | `Percent` |  |
| Change in minimum river flow (%) | Anguilla | 2015 | 128.987 | `Percent` |  |
| Change in minimum river flow (%) | Anguilla | 2016 | 130.936 | `Percent` |  |
| Change in minimum river flow (%) | Bahrain | 2019 | 155.081 | `Percent` |  |
| Change in minimum river flow (%) | Bahrain | 2020 | 171.328 | `Percent` |  |
| Change in minimum river flow (%) | Bahrain | 2021 | 179.809 | `Percent` |  |
| Change in minimum river flow (%) | Bahrain | 2022 | 143.066 | `Percent` |  |
| Change in minimum river flow (%) | Curaçao | 2013 | 137.686 | `Percent` |  |
| Change in minimum river flow (%) | Curaçao | 2014 | 140.903 | `Percent` |  |
| Change in minimum river flow (%) | Guadeloupe | 2014 | 111.213 | `Percent` |  |
| Change in minimum river flow (%) | Guadeloupe | 2015 | 106.629 | `Percent` |  |
| Change in minimum river flow (%) | Guadeloupe | 2016 | 106.244 | `Percent` |  |
| Change in minimum river flow (%) | Kiribati | 2005 | 167.621 | `Percent` |  |
| Change in minimum river flow (%) | Kiribati | 2006 | 171.125 | `Percent` |  |
| Change in minimum river flow (%) | Kiribati | 2007 | 171.139 | `Percent` |  |
| Change in minimum river flow (%) | Saint Kitts and Nevis | 2006 | 103.448 | `Percent` |  |
| Change in minimum river flow (%) | Saint Kitts and Nevis | 2007 | 111.445 | `Percent` |  |
| Change in minimum river flow (%) | Saint Kitts and Nevis | 2008 | 112.295 | `Percent` |  |
| Change in minimum river flow (%) | Saint Kitts and Nevis | 2009 | 119.286 | `Percent` |  |
| Change in minimum river flow (%) | Kuwait | 2024 | 103.454 | `Percent` |  |
| Change in minimum river flow (%) | Oman | 2013 | 173.046 | `Percent` |  |
| Change in minimum river flow (%) | Oman | 2014 | 167.543 | `Percent` |  |
| Change in minimum river flow (%) | Oman | 2015 | 168.938 | `Percent` |  |
| Change in minimum river flow (%) | Oman | 2016 | 168.257 | `Percent` |  |
| Change in minimum river flow (%) | country/QAT | 2018 | 190.554 | `Percent` |  |
| Change in minimum river flow (%) | country/QAT | 2019 | 228.333 | `Percent` |  |
| Change in minimum river flow (%) | country/QAT | 2020 | 145.267 | `Percent` |  |
| Change in minimum river flow (%) | country/QAT | 2021 | 168.466 | `Percent` |  |
| Change in minimum river flow (%) | country/QAT | 2022 | 166.106 | `Percent` |  |
| Change in minimum river flow (%) | country/SAU | 2024 | 115.452 | `Percent` |  |
| Change in minimum river flow (%) | country/VGB | 2015 | 170.853 | `Percent` |  |
| Change in minimum river flow (%) | country/VGB | 2016 | 155.613 | `Percent` |  |
| Change in maximum river flow (%) | Aruba | 2012 | 117.745 | `Percent` |  |
| Change in maximum river flow (%) | Aruba | 2013 | 125.279 | `Percent` |  |
| Change in maximum river flow (%) | United Arab Emirates | 2017 | 112.277 | `Percent` |  |
| Change in maximum river flow (%) | United Arab Emirates | 2018 | 121.539 | `Percent` |  |
| Change in maximum river flow (%) | United Arab Emirates | 2021 | 180.334 | `Percent` |  |
| Change in maximum river flow (%) | United Arab Emirates | 2022 | 128.086 | `Percent` |  |
| Change in maximum river flow (%) | United Arab Emirates | 2023 | 129.558 | `Percent` |  |
| Change in maximum river flow (%) | United Arab Emirates | 2024 | 146.407 | `Percent` |  |

## `shared_value` — MEDIUM · 175 findings

An identical value carrying 3+ decimals, in 5+ countries for the same year. Countries do not agree to that precision by chance; this is the shape of a modelled default.

*Showing the first 60 of 175. The full set is in the JSON beside this page.*

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Net outbound official development assistance (ODA) to small isla | 5 countries | 2012 | 0.0024 | `Percent` | Bulgaria, Latvia, Poland, Romania, Slovakia |
| Net outbound official development assistance (ODA) to small isla | 5 countries | 2021 | 0.0019 | `Percent` | Bulgaria, Estonia, Kuwait, Latvia, Romania |
| Alternative conversion factor used by the Development Economics  | 5 countries | 2000 | 1.08271 | `RATIO` | Andorra, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2000 | 1.08271 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +5  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2000 | 710.208 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2001 | 1.11653 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +5  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2001 | 732.398 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2002 | 1.05756 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +5  |
| Alternative conversion factor used by the Development Economics  | 12 countries | 2002 | 693.713 | `RATIO` | Benin, Burkina Faso, Central African Republic, Congo [Republic], Côte  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2003 | 0.884048 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +5  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2003 | 579.897 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2004 | 0.803922 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +5  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2004 | 527.338 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2005 | 0.8038 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +5  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2005 | 527.258 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2006 | 0.796433 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +5  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2006 | 522.426 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2007 | 0.729672 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +6  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2007 | 478.634 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2008 | 0.679923 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +6  |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2008 | 446 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2009 | 0.716958 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +6  |
| Alternative conversion factor used by the Development Economics  | 5 countries | 2009 | 0.716958 | `RATIO` | Andorra, Cyprus, Monaco, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2009 | 470.293 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2010 | 0.754309 | `RATIO` | Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy +6  |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2010 | 0.754309 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2010 | 494.794 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 15 countries | 2011 | 0.718414 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2011 | 0.718414 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2011 | 471.249 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2012 | 0.778338 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 15 countries | 2012 | 0.778338 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2012 | 510.556 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2013 | 0.752945 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 15 countries | 2013 | 0.752945 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2013 | 493.9 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2014 | 0.752728 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 16 countries | 2014 | 0.752728 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2014 | 493.757 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2015 | 0.901296 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 17 countries | 2015 | 0.901296 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2015 | 591.212 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2016 | 0.903421 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 17 countries | 2016 | 0.903421 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2016 | 592.606 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 17 countries | 2017 | 0.885206 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2017 | 0.885206 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 14 countries | 2017 | 580.657 | `RATIO` | Benin, Burkina Faso, Cameroon, Central African Republic, Congo [Republ |
| Alternative conversion factor used by the Development Economics  | 17 countries | 2018 | 0.846773 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 7 countries | 2018 | 0.846773 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Montenegro, Saint Martin, country/SMR |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2018 | 555.446 | `RATIO` | Benin, Burkina Faso, Central African Republic, Congo [Republic], Côte  |
| Alternative conversion factor used by the Development Economics  | 5 countries | 2019 | 0.893276 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Saint Martin |
| Alternative conversion factor used by the Development Economics  | 17 countries | 2019 | 0.893276 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2019 | 585.911 | `RATIO` | Benin, Burkina Faso, Central African Republic, Congo [Republic], Côte  |
| Alternative conversion factor used by the Development Economics  | 5 countries | 2020 | 0.875506 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Saint Martin |
| Alternative conversion factor used by the Development Economics  | 17 countries | 2020 | 0.875506 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2020 | 575.586 | `RATIO` | Burkina Faso, Cameroon, Central African Republic, Congo [Republic], Cô |
| Alternative conversion factor used by the Development Economics  | 5 countries | 2021 | 0.845494 | `RATIO` | Andorra, Cyprus, Malta, Monaco, Saint Martin |
| Alternative conversion factor used by the Development Economics  | 17 countries | 2021 | 0.845494 | `RATIO` | Austria, Belgium, Estonia, Finland, France, Germany, Greece, Ireland + |
| Alternative conversion factor used by the Development Economics  | 13 countries | 2021 | 554.531 | `RATIO` | Burkina Faso, Cameroon, Central African Republic, Congo [Republic], Cô |

## `flatline` — LOW · 803 findings

6+ consecutive identical non-zero values. Either nothing changed, or a figure is being carried forward.

*Showing the first 60 of 803. The full set is in the JSON beside this page.*

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Proportion of agricultural land area that has achieved an accept | Belarus | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Switzerland | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Denmark | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | United Kingdom | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Ukraine | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Belarus | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Switzerland | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | United Kingdom | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Belarus | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Switzerland | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Denmark | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | United Kingdom | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Ukraine | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Switzerland | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Denmark | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Finland | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Hungary | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Norway | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Sweden | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Denmark | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Forest area certified under an independently verified certificat | country/SUR | 2019 | 21720 | `AREA_HA` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Belarus | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Hungary | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Ukraine | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Belarus | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Switzerland | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Denmark | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Finland | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | United Kingdom | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Hungary | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Norway | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Belarus | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Switzerland | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Proportion of agricultural land area that has achieved an accept | Hungary | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Belarus | 2018 | 100 | `Percent` | 7 consecutive years 2018–2024 |
| Proportion of agricultural land area that has achieved an accept | Denmark | 2019 | 100 | `Percent` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Armenia | 2019 | 2.29 | `SCORE` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Bahrain | 2016 | 3.5 | `SCORE` | 9 consecutive years 2016–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Central African Republic | 2019 | 4.67 | `SCORE` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Comoros | 2017 | 4.29 | `SCORE` | 8 consecutive years 2017–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Germany | 2015 | 4.43 | `SCORE` | 10 consecutive years 2015–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Federated States of Micronesia | 2018 | 2.6 | `SCORE` | 7 consecutive years 2018–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Guadeloupe | 2015 | 2.6 | `SCORE` | 10 consecutive years 2015–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Equatorial Guinea | 2019 | 3.17 | `SCORE` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Iran | 2019 | 3 | `SCORE` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Nepal | 2019 | 4.43 | `SCORE` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Oman | 2019 | 4.5 | `SCORE` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Réunion | 2015 | 4.5 | `SCORE` | 10 consecutive years 2015–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Rwanda | 2019 | 4.43 | `SCORE` | 6 consecutive years 2019–2024 |
| Progress toward productive and sustainable agriculture, trend sc | Senegal | 2019 | 4.43 | `SCORE` | 6 consecutive years 2019–2024 |
| Agriculture value added share of GDP | Nauru | 2018 | 2.39 | `Percent` | 6 consecutive years 2018–2023 |
| Agriculture value added share of GDP | Singapore | 2011 | 0.03 | `Percent` | 14 consecutive years 2011–2024 |
| Agriculture value added share of GDP | Somalia | 2017 | 52.87 | `Percent` | 7 consecutive years 2017–2023 |
| Population in moderate or severe food insecurity | Grenada | 2017 | 100000 | `COUNT` | 7 consecutive years 2017–2023 |
| Population in moderate or severe food insecurity | Iceland | 2015 | 100000 | `COUNT` | 9 consecutive years 2015–2023 |
| Population in moderate or severe food insecurity | Kiribati | 2018 | 100000 | `COUNT` | 6 consecutive years 2018–2023 |
| Population in moderate or severe food insecurity | Luxembourg | 2015 | 100000 | `COUNT` | 9 consecutive years 2015–2023 |
| Population in moderate or severe food insecurity | Malta | 2015 | 100000 | `COUNT` | 9 consecutive years 2015–2023 |
| Population in moderate or severe food insecurity | Montenegro | 2015 | 100000 | `COUNT` | 9 consecutive years 2015–2023 |
| Population in moderate or severe food insecurity | Samoa | 2017 | 100000 | `COUNT` | 7 consecutive years 2017–2023 |

## `flatline_zero` — LOW · 659 findings

10+ consecutive zeros. Often true of small states; occasionally a missing value written as 0.

*Showing the first 60 of 659. The full set is in the JSON beside this page.*

| Indicator | Place | Year | Value | Unit | Detail |
|---|---|---:|---:|---|---|
| Volume of remittances as a proportion of total GDP | Andorra | 2005 | 0 | `Percent` | 14 consecutive years 2005–2018 |
| Volume of remittances as a proportion of total GDP | Bahrain | 2005 | 0 | `Percent` | 19 consecutive years 2005–2023 |
| Volume of remittances as a proportion of total GDP | Bahamas | 2005 | 0 | `Percent` | 15 consecutive years 2005–2019 |
| Volume of remittances as a proportion of total GDP | Brunei | 2005 | 0 | `Percent` | 15 consecutive years 2005–2019 |
| Volume of remittances as a proportion of total GDP | Central African Republic | 2005 | 0 | `Percent` | 19 consecutive years 2005–2023 |
| Volume of remittances as a proportion of total GDP | Cayman Islands | 2006 | 0 | `Percent` | 10 consecutive years 2006–2015 |
| Volume of remittances as a proportion of total GDP | Equatorial Guinea | 2005 | 0 | `Percent` | 19 consecutive years 2005–2023 |
| Volume of remittances as a proportion of total GDP | Iran | 2005 | 0 | `Percent` | 19 consecutive years 2005–2023 |
| Volume of remittances as a proportion of total GDP | Libya | 2007 | 0 | `Percent` | 17 consecutive years 2007–2023 |
| Volume of remittances as a proportion of total GDP | Mauritania | 2005 | 0 | `Percent` | 12 consecutive years 2005–2016 |
| Volume of remittances as a proportion of total GDP | Singapore | 2005 | 0 | `Percent` | 19 consecutive years 2005–2023 |
| Volume of remittances as a proportion of total GDP | country/SMR | 2005 | 0 | `Percent` | 12 consecutive years 2005–2016 |
| Volume of remittances as a proportion of total GDP | country/SOM | 2005 | 0 | `Percent` | 13 consecutive years 2005–2017 |
| Volume of remittances as a proportion of total GDP | country/SYR | 2011 | 0 | `Percent` | 12 consecutive years 2011–2022 |
| Volume of remittances as a proportion of total GDP | country/TCD | 2005 | 0 | `Percent` | 19 consecutive years 2005–2023 |
| Volume of remittances as a proportion of total GDP | country/TKM | 2005 | 0 | `Percent` | 19 consecutive years 2005–2023 |
| Net inbound official development assistance (ODA) to LDCs from O | Malta | 2000 | 0 | `CR_USD_K` | 11 consecutive years 2000–2010 |
| Net outbound official development assistance (ODA) to landlocked | Malta | 2000 | 0 | `CR_USD_K` | 11 consecutive years 2000–2010 |
| Net outbound official development assistance (ODA) to small isla | Malta | 2000 | 0 | `CR_USD_K` | 11 consecutive years 2000–2010 |
| Net outbound official development assistance (ODA) to small isla | Saudi Arabia | 2000 | 0 | `CR_USD_K` | 11 consecutive years 2000–2010 |
| Installed renewable electricity-generating capacity | Anguilla | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 12 consecutive years 2000–2011 |
| Installed renewable electricity-generating capacity | American Samoa | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 12 consecutive years 2000–2011 |
| Installed renewable electricity-generating capacity | Saint Barthélemy | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 16 consecutive years 2000–2015 |
| Installed renewable electricity-generating capacity | Brunei | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 10 consecutive years 2000–2009 |
| Installed renewable electricity-generating capacity | Cayman Islands | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 16 consecutive years 2000–2015 |
| Installed renewable electricity-generating capacity | Djibouti | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 10 consecutive years 2000–2009 |
| Installed renewable electricity-generating capacity | Hong Kong | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 14 consecutive years 2000–2013 |
| Installed renewable electricity-generating capacity | Saint Kitts and Nevis | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 10 consecutive years 2000–2009 |
| Installed renewable electricity-generating capacity | Kuwait | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 11 consecutive years 2000–2010 |
| Installed renewable electricity-generating capacity | Saint Martin | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 13 consecutive years 2000–2012 |
| Installed renewable electricity-generating capacity | Mauritania | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 12 consecutive years 2000–2011 |
| Installed renewable electricity-generating capacity | Montserrat | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 19 consecutive years 2000–2018 |
| Installed renewable electricity-generating capacity | Oman | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 13 consecutive years 2000–2012 |
| Installed renewable electricity-generating capacity | country/QAT | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 11 consecutive years 2000–2010 |
| Installed renewable electricity-generating capacity | country/SEN | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 10 consecutive years 2000–2009 |
| Installed renewable electricity-generating capacity | country/SPM | 2015 | 0 | `RATIO_POWER_W_PER_POP` | 10 consecutive years 2015–2024 |
| Installed renewable electricity-generating capacity | country/SSD | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 11 consecutive years 2000–2010 |
| Installed renewable electricity-generating capacity | country/SXM | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 25 consecutive years 2000–2024 |
| Installed renewable electricity-generating capacity | country/SYC | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 13 consecutive years 2000–2012 |
| Installed renewable electricity-generating capacity | country/TCA | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 15 consecutive years 2000–2014 |
| Installed renewable electricity-generating capacity | country/TKL | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 12 consecutive years 2000–2011 |
| Installed renewable electricity-generating capacity | country/VGB | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 10 consecutive years 2000–2009 |
| Installed renewable electricity-generating capacity | country/VIR | 2000 | 0 | `RATIO_POWER_W_PER_POP` | 11 consecutive years 2000–2010 |
| Share of renewable energy in the total final energy consumption | American Samoa | 1990 | 0 | `Percent` | 22 consecutive years 1990–2011 |
| Share of renewable energy in the total final energy consumption | Antigua and Barbuda | 1990 | 0 | `Percent` | 10 consecutive years 1990–1999 |
| Share of renewable energy in the total final energy consumption | Bahrain | 1990 | 0 | `Percent` | 28 consecutive years 1990–2017 |
| Share of renewable energy in the total final energy consumption | Brunei | 1993 | 0 | `Percent` | 18 consecutive years 1993–2010 |
| Share of renewable energy in the total final energy consumption | Cayman Islands | 1990 | 0 | `Percent` | 19 consecutive years 1990–2008 |
| Share of renewable energy in the total final energy consumption | Falkland Islands | 1990 | 0 | `Percent` | 18 consecutive years 1990–2007 |
| Share of renewable energy in the total final energy consumption | Guernsey | 1990 | 0 | `Percent` | 28 consecutive years 1990–2017 |
| Share of renewable energy in the total final energy consumption | Gibraltar | 1990 | 0 | `Percent` | 34 consecutive years 1990–2023 |
| Share of renewable energy in the total final energy consumption | Jersey | 1990 | 0 | `Percent` | 12 consecutive years 1990–2001 |
| Share of renewable energy in the total final energy consumption | Malta | 1990 | 0 | `Percent` | 12 consecutive years 1990–2001 |
| Share of renewable energy in the total final energy consumption | Northern Mariana Islands | 1992 | 0 | `Percent` | 28 consecutive years 1992–2019 |
| Share of renewable energy in the total final energy consumption | Montserrat | 1990 | 0 | `Percent` | 29 consecutive years 1990–2018 |
| Share of renewable energy in the total final energy consumption | country/NRU | 1990 | 0 | `Percent` | 16 consecutive years 1990–2005 |
| Share of renewable energy in the total final energy consumption | country/OMN | 1990 | 0 | `Percent` | 27 consecutive years 1990–2016 |
| Share of renewable energy in the total final energy consumption | country/PLW | 1992 | 0 | `Percent` | 22 consecutive years 1992–2013 |
| Share of renewable energy in the total final energy consumption | country/SPM | 1990 | 0 | `Percent` | 10 consecutive years 1990–1999 |
| Share of renewable energy in the total final energy consumption | country/TUV | 1990 | 0 | `Percent` | 10 consecutive years 1990–1999 |

## Suppressed as structural

A rule violated by most of an indicator's observations is not a violation, it is the definition. These (indicator, check) pairs fired often enough to be structural and were dropped from the findings above — listed here because the list is itself a result.

**165 suppressed groups** covering 38,943 would-be findings.

### `jump` — 71 indicators

| Indicator | Unit | Fired | Of | Share |
|---|---|---:|---:|---:|
| International financial flows to developing countries in support of clea | `CR_USD_K` | 586 | 3,800 observations | 15% |
| Total inbound official development assistance for biodiversity | `CR_USD_K` | 391 | 3,003 observations | 13% |
| Direct economic loss attributed to disasters | `CR_USD` | 259 | 1,769 observations | 15% |
| Direct economic loss attributed to disasters relative to GDP | `Percent` | 258 | 1,769 observations | 15% |
| Number of directly affected persons attributed to disasters per 100,000  | `RATIO_COUNT_PER_100000_COUNT_POP` | 250 | 1,955 observations | 13% |
| Number of people affected by disasters | `COUNT` | 247 | 1,955 observations | 13% |
| Chlorophyll-a deviations, remote sensing | `Percent` | 244 | 3,448 observations | 7% |
| Gross receipts by developing countries of mobilised private finance (MPF | `CR_USD` | 228 | 1,066 observations | 21% |
| Direct economic loss in the housing sector attributed to disasters | `CR_USD` | 224 | 1,625 observations | 14% |
| Number of people whose damaged dwellings were attributed to disasters | `COUNT` | 208 | 1,621 observations | 13% |
| Number of people whose destroyed dwellings were attributed to disasters | `COUNT` | 183 | 1,415 observations | 13% |
| Total inbound official flows (commitments) for Aid for Trade | `CR_USD_K` | 172 | 2,624 observations | 7% |
| Number of injured or ill people attributed to disasters | `COUNT` | 169 | 1,808 observations | 9% |
| Number of deaths and missing persons attributed to disasters per 100,000 | `RATIO_COUNT_PER_100000_COUNT_POP` | 160 | 2,122 observations | 8% |
| Number of deaths and missing persons attributed to disasters | `COUNT` | 156 | 2,122 observations | 7% |
| Number of deaths due to disaster | `COUNT` | 149 | 2,107 observations | 7% |
| Beach litter items per unit of surface area (Number of items per 100 squ | `RATIO_COUNT_PER_100_AREA_M2` | 146 | 971 observations | 15% |
| Number of people whose livelihoods were disrupted or destroyed, attribut | `COUNT` | 115 | 1,051 observations | 11% |
| Total inbound official development assistance to medical research and ba | `CR_USD_K` | 107 | 3,333 observations | 3% |
| Direct agriculture loss attributed to disasters | `CR_USD` | 106 | 778 observations | 14% |
| Direct economic loss resulting from damaged or destroyed critical infras | `CR_USD` | 97 | 1,138 observations | 9% |
| Monetary amount committed to public-private partnerships for infrastruct | `CR_USD` | 90 | 2,683 observations | 3% |
| Monetary amount committed to public-private partnerships for infrastruct | `CR_USD_K` | 89 | 2,605 observations | 3% |
| Number of damaged critical infrastructure attributed to disasters | `COUNT` | 86 | 855 observations | 10% |
| Number of people requiring interventions against neglected tropical dise | `COUNT` | 84 | 2,910 observations | 3% |
| Total official development assistance (gross disbursement) for technical | `CR_USD_K` | 75 | 3,529 observations | 2% |
| Number of disruptions to basic services attributed to disasters | `COUNT` | 74 | 891 observations | 8% |
| Gross receipts by developing countries of private grants | `CR_USD` | 70 | 1,073 observations | 7% |
| Total deaths and disappearances recorded during migration | `COUNT` | 69 | 821 observations | 8% |
| Number of destroyed or damaged educational facilities attributed to disa | `COUNT` | 62 | 748 observations | 8% |
| Inbound official development assistance grants for poverty reduction, as | `Percent` | 61 | 3,350 observations | 2% |
| Gross receipts by developing countries of official concessional sustaina | `CR_USD` | 61 | 807 observations | 8% |
| Number of transboundary breeds with unknown risk status (number) | `COUNT` | 51 | 4,772 observations | 1% |
| Number of missing persons due to disaster | `COUNT` | 47 | 1,489 observations | 3% |
| Total inbound official flows for scholarships | `CR_USD_K` | 45 | 2,554 observations | 2% |
| Hazardous waste exported | `WEIGHT_TN` | 42 | 1,148 observations | 4% |
| Amount of tracked exported Environmentally Sound Technologies | `CR_USD` | 41 | 2,430 observations | 2% |
| Number of disruptions to health services attributed to disasters | `COUNT` | 39 | 688 observations | 6% |
| Gross receipts by developing countries of official non-concessional sust | `CR_USD` | 33 | 796 observations | 4% |
| Number of destroyed or damaged health facilities attributed to disasters | `COUNT` | 33 | 628 observations | 5% |
| Amount of tracked re-imported Environmentally Sound Technologies | `CR_USD` | 30 | 602 observations | 5% |
| Hazardous waste imported | `WEIGHT_TN` | 30 | 1,021 observations | 3% |
| Number of disruptions to educational services attributed to disasters | `COUNT` | 30 | 731 observations | 4% |
| Total inbound official flows (disbursement) for Aid for Trade | `CR_USD_K` | 29 | 2,624 observations | 1% |
| Amount of tracked re-exported Environmentally Sound Technologies | `CR_USD` | 28 | 824 observations | 3% |
| Number of disruptions to other basic services attributed to disasters | `COUNT` | 28 | 564 observations | 5% |
| Detected victims of human trafficking | `COUNT` | 28 | 1,792 observations | 2% |
| Total outbound official development assistance for biodiversity | `CR_USD_K` | 26 | 566 observations | 5% |
| Detected victims of human trafficking (per 100,000 population) | `RATIO_COUNT_PER_100000_COUNT_POP` | 26 | 1,792 observations | 1% |
| Number of other destroyed or damaged critical infrastructure units and f | `COUNT` | 23 | 470 observations | 5% |
| Hazardous waste treated or disposed | `WEIGHT_TN` | 22 | 986 observations | 2% |
| Direct economic loss to other damaged or destroyed productive assets att | `CR_USD` | 20 | 835 observations | 2% |
| Total outbound official flows (commitments) for Aid for Trade | `CR_USD_K` | 19 | 629 observations | 3% |
| Total outbound official flows (disbursement) for Aid for Trade | `CR_USD_K` | 19 | 629 observations | 3% |
| Proportion of hazardous waste that is treated or disposed | `Percent` | 19 | 900 observations | 2% |
| Detected victims of human trafficking for forced labour, servitude and s | `COUNT` | 17 | 1,204 observations | 1% |
| Detected victims of human trafficking for forced labour, servitude and s | `RATIO_COUNT_PER_100000_COUNT_POP` | 16 | 1,204 observations | 1% |
| Detected victims of human trafficking for other purposes | `COUNT` | 15 | 1,250 observations | 1% |
| Hazardous waste generated, per capita | `WEIGHT_KG` | 14 | 1,298 observations | 1% |
| Detected victims of human trafficking for other purposes (per 100,000 po | `RATIO_COUNT_PER_100000_COUNT_POP` | 14 | 1,250 observations | 1% |
| Outbound official development assistance grants for poverty reduction, a | `Percent` | 12 | 726 observations | 2% |
| Net outbound official development assistance (ODA) to small island state | `Percent` | 12 | 949 observations | 1% |
| Number of local governments that adopt and implement local disaster-risk | `COUNT` | 12 | 888 observations | 1% |
| Proportion of the target population who received the final dose of human | `Percent` | 12 | 1,129 observations | 1% |
| Direct economic loss to cultural heritage damaged or destroyed attribute | `CR_USD` | 12 | 793 observations | 2% |
| Gross receipts by developing countries of official sustainable developme | `CR_USD` | 11 | 898 observations | 1% |
| Agricultural export subsidies | `CR_USD` | 8 | 635 observations | 1% |
| Total electronic waste collected | `WEIGHT_TN` | 8 | 785 observations | 1% |
| Electronic waste generated per capita | `WEIGHT_KG` | 4 | 352 observations | 1% |
| Total electronic waste generated | `WEIGHT_TN` | 4 | 352 observations | 1% |
| [World Bank] Proportion of population covered by labour market programs | `Percent` | 4 | 294 observations | 1% |

### `flatline` — 37 indicators

| Indicator | Unit | Fired | Of | Share |
|---|---|---:|---:|---:|
| Number of transboundary breeds (not extinct) (number) | `COUNT` | 274 | 193 series | 142% |
| Number of transboundary breeds (including extinct ones) | `COUNT` | 271 | 193 series | 140% |
| Average proportion of Terrestrial Key Biodiversity Areas (KBAs) covered  | `Percent` | 262 | 241 series | 109% |
| Number of transboundary breeds with unknown risk status (number) | `COUNT` | 255 | 193 series | 132% |
| Number of local breeds kept in the country | `COUNT` | 254 | 187 series | 136% |
| Number of local breeds (not extinct) | `COUNT` | 248 | 186 series | 133% |
| Average proportion of Marine Key Biodiversity Areas (KBAs) covered by pr | `Percent` | 218 | 191 series | 114% |
| Number of local breeds with unknown risk status | `COUNT` | 212 | 186 series | 114% |
| Average proportion of Mountain Key Biodiversity Areas (KBAs) covered by  | `Percent` | 206 | 184 series | 112% |
| Average proportion of Freshwater Key Biodiversity Areas (KBAs) covered b | `Percent` | 180 | 164 series | 110% |
| Countries with death registration data that are at least 75 percent comp | `COUNT` | 151 | 194 series | 78% |
| Countries that are contracting Parties to the International Treaty on Pl | `COUNT` | 146 | 246 series | 59% |
| Countries with birth registration data that are at least 90 percent comp | `COUNT` | 146 | 197 series | 74% |
| Proportion of population covered by at least a 2G mobile network | `Percent` | 126 | 225 series | 56% |
| Countries with national statistical legislation that complies with the F | `COUNT` | 118 | 195 series | 61% |
| Proportion of population with access to electricity | `Percent` | 113 | 217 series | 52% |
| Countries with National Human Rights Institutions in compliance with the | `COUNT` | 105 | 194 series | 54% |
| Countries with national statistical plans that are under implementation | `COUNT` | 100 | 200 series | 50% |
| Level of water stress: freshwater withdrawal as a proportion of availabl | `Percent` | 91 | 182 series | 50% |
| Level of national compliance with labour rights (freedom of association  | `SCORE` | 87 | 187 series | 47% |
| Implementation of standard accounting tools to monitor the economic and  | `COUNT` | 86 | 176 series | 49% |
| Implementation of standard accounting tools to monitor the economic and  | `COUNT` | 78 | 176 series | 44% |
| Proportion of countries with independent National Human Rights Instituti | `Percent` | 77 | 194 series | 40% |
| Proportion of local breeds classified as being at risk of extinction as  | `Percent` | 74 | 156 series | 47% |
| Current number of seats in national parliaments | `COUNT` | 68 | 191 series | 36% |
| Proportion of transboundary breeds classified as being at risk of extinc | `Percent` | 64 | 145 series | 44% |
| Proportion of population covered by at least a 3G mobile network | `Percent` | 62 | 224 series | 28% |
| Number of undernourished people | `COUNT` | 62 | 138 series | 45% |
| Countries with national statistical plans that are fully funded | `COUNT` | 60 | 183 series | 33% |
| Prevalence of undernourishment | `Percent` | 59 | 169 series | 35% |
| Proportion of the target population who received 3 doses of diphtheria-t | `Percent` | 58 | 194 series | 30% |
| Number of local governments | `COUNT` | 54 | 132 series | 41% |
| Progress toward productive and sustainable agriculture, current status s | `SCORE` | 50 | 195 series | 26% |
| Implementation of standard accounting tools to monitor the economic and  | `COUNT` | 50 | 172 series | 29% |
| Countries with national statistical plans with funding from government | `COUNT` | 46 | 176 series | 26% |
| Plant genetic resources accessions stored ex situ | `COUNT` | 37 | 118 series | 31% |
| Proportion of agricultural land area that has achieved an acceptable or  | `Percent` | 9 | 35 series | 26% |

### `percent_negative` — 23 indicators

| Indicator | Unit | Fired | Of | Share |
|---|---|---:|---:|---:|
| Current account balance as a proportion of GDP | `Percent` | 2,871 | 4,378 observations | 66% |
| Cash surplus/deficit as a proportion of GDP | `Percent` | 2,811 | 2,841 observations | 99% |
| Change in minimum river flow (%) | `Percent` | 2,142 | 4,220 observations | 51% |
| Change in maximum river flow (%) | `Percent` | 2,060 | 4,220 observations | 49% |
| Change in seasonal water area of lakes and rivers | `Percent` | 1,371 | 4,158 observations | 33% |
| Annual growth rate of real GDP per capita | `Percent` | 1,256 | 5,210 observations | 24% |
| Annual growth of the gross capital formation | `Percent` | 1,239 | 3,698 observations | 34% |
| Annual growth of exports of goods and services | `Percent` | 1,118 | 3,937 observations | 28% |
| Change in minimum reservoir water area | `Percent` | 1,110 | 3,266 observations | 34% |
| Annual growth of imports of goods and services | `Percent` | 1,097 | 3,937 observations | 28% |
| Change in permanent water area of lakes and rivers | `Percent` | 1,020 | 4,194 observations | 24% |
| Annual GDP growth | `Percent` | 843 | 5,130 observations | 16% |
| Annual growth of final consumption expenditure of the general government | `Percent` | 803 | 3,793 observations | 21% |
| Mangrove total area change | `Percent` | 768 | 1,160 observations | 66% |
| Annual growth of final consumption expenditure of households and non-pro | `Percent` | 614 | 3,870 observations | 16% |
| Foreign direct investment, net inflows, as a proportion of GDP | `Percent` | 351 | 4,796 observations | 7% |
| Ratio of net open position in foreign exchange to capital | `Percent` | 331 | 1,805 observations | 18% |
| Annual inflation (consumer prices) | `Percent` | 322 | 4,494 observations | 7% |
| Ratio of non-performing loans (net of provisions) to capital | `Percent` | 313 | 2,199 observations | 14% |
| Annual forest area change rate | `Percent` | 281 | 684 observations | 41% |
| Annual growth of broad money | `Percent` | 246 | 3,745 observations | 7% |
| Rate of return on assets | `Percent` | 132 | 2,292 observations | 6% |
| Growth rates of household expenditure or income per capita | `Percent` | 35 | 121 observations | 29% |

### `flatline_zero` — 18 indicators

| Indicator | Unit | Fired | Of | Share |
|---|---|---:|---:|---:|
| Forest area certified under an independently verified certification sche | `AREA_HA` | 155 | 246 series | 63% |
| Countries that have legislative, administrative and policy framework or  | `COUNT` | 149 | 246 series | 61% |
| Implementation of standard accounting tools to monitor the economic and  | `COUNT` | 105 | 172 series | 61% |
| Countries that are contracting Parties to the International Treaty on Pl | `COUNT` | 100 | 246 series | 41% |
| Minimum reservoir water area | `AREA_KM2` | 97 | 236 series | 41% |
| Maxiumum reservoir water area | `AREA_KM2` | 97 | 236 series | 41% |
| Proportion of countries with independent National Human Rights Instituti | `Percent` | 97 | 194 series | 50% |
| Implementation of standard accounting tools to monitor the economic and  | `COUNT` | 76 | 176 series | 43% |
| Countries with National Human Rights Institutions in compliance with the | `COUNT` | 75 | 194 series | 39% |
| Minimum reservoir water area as a proportion of total land area | `Percent` | 73 | 209 series | 35% |
| Maximum reservoir water area as a proportion of total land area | `Percent` | 72 | 209 series | 34% |
| Proportion of population practicing open defecation | `Percent` | 72 | 232 series | 31% |
| Total reported number of Standard Material Transfer Agreements (SMTAs) t | `COUNT` | 63 | 246 series | 26% |
| Implementation of standard accounting tools to monitor the economic and  | `COUNT` | 61 | 176 series | 35% |
| Proportion of transboundary breeds classified as being at risk of extinc | `Percent` | 54 | 145 series | 37% |
| Monetary amount committed to public-private partnerships for infrastruct | `CR_USD` | 54 | 128 series | 42% |
| Monetary amount committed to public-private partnerships for infrastruct | `CR_USD_K` | 52 | 128 series | 41% |
| Agricultural export subsidies | `CR_USD` | 9 | 33 series | 27% |

### `percent_over_100` — 16 indicators

| Indicator | Unit | Fired | Of | Share |
|---|---|---:|---:|---:|
| Primary government expenditures as a proportion of original approved bud | `Percent` | 1,000 | 2,484 observations | 40% |
| Merchandise trade as a proportion of GDP | `Percent` | 681 | 4,963 observations | 14% |
| Level of water stress: freshwater withdrawal as a proportion of availabl | `Percent` | 371 | 4,223 observations | 9% |
| Ratio of liquid assets to short term liabilities | `Percent` | 301 | 2,128 observations | 14% |
| External debt stocks as a proportion of GNI | `Percent` | 290 | 2,899 observations | 10% |
| Change in seasonal water area of lakes and rivers | `Percent` | 245 | 4,158 observations | 6% |
| Proportion of hazardous waste that is treated or disposed | `Percent` | 142 | 900 observations | 16% |
| Change in permanent water area of lakes and rivers | `Percent` | 134 | 4,194 observations | 3% |
| Ratio of net open position in foreign exchange to capital | `Percent` | 117 | 1,805 observations | 6% |
| Gross public sector debt, Central Government, as a proportion of GDP | `Percent` | 100 | 1,023 observations | 10% |
| Change in minimum reservoir water area | `Percent` | 68 | 3,266 observations | 2% |
| Proportion of domestic budget funded by domestic taxes | `Percent` | 57 | 3,282 observations | 2% |
| Ratio of non-performing loans (net of provisions) to capital | `Percent` | 55 | 2,199 observations | 2% |
| Foreign direct investment, net inflows, as a proportion of GDP | `Percent` | 54 | 4,796 observations | 1% |
| Proportion of wastewater treated | `Percent` | 14 | 72 observations | 19% |
| Proportion of population that feel safe walking alone around the area th | `Percent` | 3 | 258 observations | 1% |


## Reproducing

```bash
python3 probe/smell.py
```

One `get_child_observations` call per indicator returns every country and every year, so the whole sweep is a few hundred calls.

