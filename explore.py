"""A quick, neutral tour of the Northwind Outdoor dataset.

Run it to orient yourself before you dig in:

    uv run python explore.py

This only describes what's in the data (shapes, ranges, a few distributions and joins). It does
not tell you what to build. Full column docs are in DATA_DICTIONARY.md.
"""
import pandas as pd

from harness.load_data import TABLES, load_table

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def rule(title: str) -> None:
    print("\n" + "=" * 78 + f"\n{title}\n" + "=" * 78)


def main() -> None:
    rule("TABLES AT A GLANCE")
    for name in TABLES:
        df = load_table(name)
        print(f"{name:16s} {df.shape[0]:>7,} rows x {df.shape[1]:>2} cols  |  {', '.join(df.columns)}")

    # ---- Dimensions ---------------------------------------------------------
    prod = load_table("dim_product")
    rule("PRODUCTS (dim_product)")
    print("Categories:", prod.category.value_counts().to_dict())
    print("Lifecycle stages:", prod.lifecycle_stage.value_counts().to_dict())
    print("Replacement chains (replaces_product_id set):")
    repl = prod[prod.replaces_product_id.notna()][["product_id", "subcategory", "replaces_product_id"]]
    print(repl.to_string(index=False) if len(repl) else "  (none)")
    print("\nSample products:")
    print(prod[["product_id", "subcategory", "lifecycle_stage", "status_code",
                "launch_date", "discontinue_date", "list_price"]].head(8).to_string(index=False))

    rule("CUSTOMERS & SITES")
    print(load_table("dim_customer").to_string(index=False))
    print()
    print(load_table("dim_site").to_string(index=False))

    # ---- Sell-through + promo lift -----------------------------------------
    pos = load_table("fact_pos")
    rule("POS / SELL-THROUGH (fact_pos)")
    print("Weeks:", pos.week.min().date(), "->", pos.week.max().date(), f"| {pos.week.nunique()} weeks")
    promoted = pos[pos.incremental_units > 0]
    print(f"Promo weeks (incremental_units > 0): {len(promoted):,} of {len(pos):,} rows")
    if len(promoted):
        lift = (promoted.incremental_units / promoted.base_units.clip(lower=1)).mean()
        print(f"Mean promo lift over base on those weeks: {lift:.0%}")

    # ---- Promo calendar -----------------------------------------------------
    promo = load_table("fact_promo")
    dim_promo = load_table("dim_promo")
    rule("PROMO CALENDAR (fact_promo + dim_promo)")
    print("Mechanics:", dim_promo.mechanic.value_counts().to_dict())
    today = pos.week.max()
    fwd = promo[promo.week > today]
    print(f"Promo rows: {len(promo):,}  |  forward-dated (after {today.date()}): {len(fwd):,}")

    # ---- Forecast vs actuals ------------------------------------------------
    fc = load_table("fact_forecast")
    rule("FORECAST (fact_forecast)")
    print(f"Snapshots (vintages): {fc.snapshot_date.nunique()}  |  weeks {fc.week.min().date()} -> {fc.week.max().date()}")
    print("Columns: baseline_qty, promo_uplift_qty, final_forecast_qty, actual_qty")
    scored = fc[fc.actual_qty.notna()].copy()
    if len(scored):
        scored["ape"] = (scored.final_forecast_qty - scored.actual_qty).abs() / scored.actual_qty.clip(lower=1)
        print(f"Rows with realized actuals (for backtesting): {len(scored):,}")
        print(f"Baseline error vs actuals (mean APE): {scored.ape.mean():.0%}")

    rule("INVENTORY & PRICING")
    print("fact_inventory cols: product_id, site_id, week, on_hand, in_transit")
    print("fact_pricing cols:   product_id, customer_id, week, list_price, promo_price, msrp")
    print("\nDone. See DATA_DICTIONARY.md for full column definitions and the vision deck (vision.html) for context.")


if __name__ == "__main__":
    main()
