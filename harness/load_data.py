"""Tidy loaders for the Northwind Outdoor demand-planning dataset.

Each loader returns a pandas DataFrame with dates parsed. `load_all()` returns a dict of every
table. Import these in your own code or let the starter agent (`agent.py`) use them.
"""
from __future__ import annotations

import functools
import os

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# table name -> list of columns that should be parsed as dates
_DATE_COLUMNS = {
    "dim_product": ["launch_date", "discontinue_date"],
    "dim_promo": ["start_date", "end_date"],
    "dim_calendar": ["date"],
    "fact_pos": ["week"],
    "fact_promo": ["week"],
    "fact_pricing": ["week"],
    "fact_shipments": ["week"],
    "fact_inventory": ["week"],
    "fact_forecast": ["snapshot_date", "week"],
}

TABLES = [
    "dim_product", "dim_site", "dim_customer", "dim_promo", "dim_calendar",
    "fact_pos", "fact_promo", "fact_pricing", "fact_shipments", "fact_inventory",
    "fact_forecast",
]


@functools.lru_cache(maxsize=None)
def load_table(name: str) -> pd.DataFrame:
    """Load a single table by name (cached)."""
    if name not in TABLES:
        raise ValueError(f"Unknown table '{name}'. Available: {', '.join(TABLES)}")
    df = pd.read_csv(os.path.join(DATA_DIR, f"{name}.csv"))
    for col in _DATE_COLUMNS.get(name, []):
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def load_all() -> dict[str, pd.DataFrame]:
    """Load every table into a dict keyed by table name."""
    return {name: load_table(name) for name in TABLES}


if __name__ == "__main__":
    for name, df in load_all().items():
        print(f"{name:16s} {df.shape[0]:>7,} rows  x {df.shape[1]} cols")
