"""
Download the Eurostat data for "Should a young Greek stay or leave?"

Run from the project folder with the .venv active:
    python get_eurostat.py

Saves one tidy CSV per dataset in data/ and prints what each one contains,
so we can confirm the dataset codes, years and age bands.
"""
from pathlib import Path

import eurostat
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Country, NUTS 1 and NUTS 2 codes we care about
GEOS = {
    "EL", "IT",            # Greece, Italy
    "EL3", "ITC",          # NUTS 1: Attiki, Nord-Ovest (Turin + Milan)
    "EL30", "ITC1", "ITC4" # NUTS 2: Attiki, Piemonte, Lombardia
}

DATASETS = {
    "wages_by_job":       "earn_ses22_48",   # SES 2022, monthly earnings by occupation
    "wages_by_region":    "earn_ses22_rhr",  # SES 2022, hourly earnings by NUTS 1
    "wages_national_hourly": "earn_ses22_14", # SES 2022, hourly earnings by age and occupation (country totals)
    "youth_unemployment": "lfst_r_lfu3rt",   # LFS, unemployment by age and NUTS 2
    "price_levels":       "prc_ppp_ind",     # price level indices
}

# Columns worth listing so we can see which codes exist
SHOW_COLUMNS = ["unit", "isco08", "age", "sex", "nace_r2", "na_item", "ppp_cat", "indic_se", "isced11"]


def to_long(df: pd.DataFrame) -> pd.DataFrame:
    """Turn Eurostat's wide table (one column per year) into one row per value."""
    geo_col = next(c for c in df.columns if str(c).startswith("geo"))
    df = df.rename(columns={geo_col: "geo"})
    year_cols = [c for c in df.columns if str(c)[:4].isdigit()]
    id_cols = [c for c in df.columns if c not in year_cols]
    long = df.melt(id_vars=id_cols, value_vars=year_cols,
                   var_name="period", value_name="value")
    return long.dropna(subset=["value"])


def main() -> None:
    for name, code in DATASETS.items():
        print(f"\n=== {name} ({code}) ===")
        try:
            raw = eurostat.get_data_df(code)
        except Exception as err:
            print(f"  FAILED to download: {err}")
            continue

        long = to_long(raw)
        long = long[long["geo"].isin(GEOS)]
        if "sex" in long.columns:
            long = long[long["sex"] == "T"]

        if long.empty:
            print("  No rows for our countries/regions. Codes in this dataset may differ.")
            continue

        out = DATA_DIR / f"{name}.csv"
        long.to_csv(out, index=False)

        print(f"  Saved {len(long):,} rows to {out.name}")
        print(f"  Regions found: {sorted(long['geo'].unique())}")
        print(f"  Periods: {long['period'].min()} to {long['period'].max()}")
        for col in SHOW_COLUMNS:
            if col in long.columns and col != "sex":
                values = sorted(long[col].astype(str).unique())
                shown = values if len(values) <= 25 else values[:25] + ["..."]
                print(f"  {col}: {shown}")


if __name__ == "__main__":
    main()
