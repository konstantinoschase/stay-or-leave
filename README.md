# Should a young Greek stay or leave?

A data project comparing life for young people in **Greece and Italy**, built from official statistics (Eurostat, OECD, ISTAT, INPS, Agenzia delle Entrate). It is neutral and factual: no opinions on parties or governments, just the numbers, with every source and year shown.

> 🚧 **Work in progress** (started November 2026). The data pipeline is being built first; the calculator page comes next.

## What it will show

A personal calculator: enter your age band, job type, net monthly salary and housing type, and compare **Athens** with **Turin** or **Milan**:

| Result | Data |
|---|---|
| Your salary in the other city | Eurostat Structure of Earnings Survey 2022, INPS |
| Money left after rent | OMI (Italy), Spitogatos (Greece) |
| Years of salary to buy a 70 m² flat | OMI (Italy), Spitogatos (Greece) |
| Youth unemployment where you'd live | Eurostat Labour Force Survey (NUTS 2 regions) |
| Real wage growth over 10 years | OECD |

Later sections: Greek emigration since the crisis, and a simple projection of when Greek wages could catch up with Italy's.

## Project structure

```
get_eurostat.py   downloads and cleans the Eurostat datasets
data/             tidy CSV files, one per dataset
```

## Run it yourself

Requires Python 3.10 or newer.

```
python3 -m venv .venv
source .venv/bin/activate
pip install eurostat pandas
python get_eurostat.py
```

## Data sources

| Dataset | Code | Coverage |
|---|---|---|
| Earnings by occupation | `earn_ses22_48` | Greece, Italy, 2022 |
| Hourly earnings by region | `earn_ses22_rhr` | Attica, Nord-Ovest, 2022 |
| Hourly earnings, national | `earn_ses22_14` | Greece, Italy, 2022 |
| Unemployment by age and region | `lfst_r_lfu3rt` | Attica, Piemonte, Lombardia, 1999–2025 |
| Price level indices | `prc_ppp_ind` | Greece, Italy, 1995–2024 |

All Eurostat data © European Union, reused under the [Eurostat copyright policy](https://ec.europa.eu/eurostat/about-us/policies/copyright).

## Author

Konstantinos Fatouros, Economics and Finance with Data Science (EFDS), University of Turin.
