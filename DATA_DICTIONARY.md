# Data dictionary — Northwind Outdoor

A synthetic demand-planning dataset for a fictional outdoor & recreation gear manufacturer,
**Northwind Outdoor**, selling through five retail customers. Eleven CSVs in `data/`: five
dimensions and six weekly fact tables. All data is generated and fictional.

**Grain:** facts are weekly (every `week` / `date` is a Monday). Where a fact spans products,
sites, customers, and time, those are its keys. History runs ~3 years; the promo calendar and
forecast horizon extend ~6 months into the future.

> **Format note.** In a production planning platform, the weekly facts below (POS, promotions,
> pricing, on-hand) are typically stored as one long "time-series" table keyed by a series name.
> Here we ship clean, separate per-fact tables for convenience.

---

## Dimensions

### `dim_product` — one row per product (SKU)
| column | type | meaning |
|---|---|---|
| `product_id` | str | SKU identifier (e.g. `NWO-1001`) |
| `name` | str | Product name |
| `brand` | str | Brand (Northwind Outdoor) |
| `category` | str | Category (Camp & Hike, Cycling, Water Sports, Apparel) |
| `subcategory` | str | Subcategory (e.g. Tents, Bike Helmets, Kayaks) |
| `status_code` | str | `Active` or `Inactive` |
| `lifecycle_stage` | str | `NPI`, `Growth`, `Mature`, or `EOL` |
| `launch_date` | date | First sale date (blank for products launched before the data window) |
| `discontinue_date` | date | Planned/actual end-of-life date (blank if not applicable) |
| `replaces_product_id` | str | If this SKU replaces another, the `product_id` it replaces (blank otherwise) |
| `std_unit_cost` | float | Standard unit cost (USD) |
| `list_price` | float | List price (USD) |

Example: `NWO-1001, Northwind Outdoor Tents T897, Northwind Outdoor, Camp & Hike, Tents, Active, Growth, , , , 78.30, 199.65`

### `dim_site` — one row per internal site
| column | type | meaning |
|---|---|---|
| `site_id` | str | Site identifier (`PLANT_01`, `DC_NORTH`, `DC_SOUTH`, `DC_WEST`) |
| `name` | str | Site name |
| `geo` | str | State/region |
| `country` | str | Country |
| `channel` | str | `Plant` or `DC` |

### `dim_customer` — one row per retail customer
| column | type | meaning |
|---|---|---|
| `customer_id` | str | Customer identifier (e.g. `CUST_MEGA`) |
| `retailer_name` | str | Retailer name (MegaMart, ClubCo, HomeNest, ShopStream, DirectWeb) |
| `country` | str | Country |

### `dim_promo` — one row per promotion event
| column | type | meaning |
|---|---|---|
| `promo_id` | str | Promotion identifier |
| `name` | str | Human-readable label |
| `mechanic` | str | `TPR`, `Feature`, `Display`, or `Coupon` |
| `discount_depth_pct` | float | Discount depth as a fraction (e.g. `0.20` = 20% off) |
| `funding_type` | str | `Vendor` or `Retailer` |
| `start_date` | date | Promo start (Monday) |
| `end_date` | date | Promo end (Monday) |

### `dim_calendar` — one row per week
| column | type | meaning |
|---|---|---|
| `date` | date | Week start (Monday) |
| `iso_week` | str | ISO year-week (e.g. `2026-W22`) |
| `fiscal_period` | str | Fiscal period label |
| `holiday_flag` | int | `1` if the week falls in the Nov/Dec holiday period |
| `season` | str | `Holiday`, `Post-Holiday`, `Summer`, or `Regular` |

---

## Facts (weekly)

### `fact_pos` — retail sell-through (consumer purchases)
Grain: product × customer × site × week.
| column | type | meaning |
|---|---|---|
| `product_id`, `customer_id`, `site_id`, `week` | keys | |
| `pos_units` | int | Units sold to consumers |
| `pos_dollars` | float | Sell-through revenue (USD) |
| `base_units` | int | Non-promoted baseline portion of `pos_units` |
| `incremental_units` | int | Promotion-driven portion of `pos_units` (`pos_units − base_units`) |

### `fact_shipments` — sell-in shipments (plant → DC)
Grain: product × from_site × to_site × week.
| column | type | meaning |
|---|---|---|
| `product_id`, `from_site_id`, `to_site_id`, `week` | keys | |
| `ship_qty` | int | Units shipped |
| `ship_value` | float | Shipment value at standard cost (USD) |

### `fact_promo` — promotion calendar (past and forward)
Grain: product × customer × promo × week. Covers historical promo weeks and the forward calendar.
| column | type | meaning |
|---|---|---|
| `product_id`, `customer_id`, `promo_id`, `week` | keys | |
| `on_promo` | int | `1` when the product/customer is on promotion that week |
| `planned_lift_pct` | float | Planned incremental lift as a fraction of base |
| `actual_lift_pct` | float | Realized lift (blank for forward weeks with no actuals yet) |
| `promo_price` | float | Promoted price (blank for forward weeks) |

### `fact_pricing` — weekly price points
Grain: product × customer × week.
| column | type | meaning |
|---|---|---|
| `product_id`, `customer_id`, `week` | keys | |
| `list_price` | float | List price (USD) |
| `promo_price` | float | Effective price that week (equals list when not on promo) |
| `msrp` | float | Manufacturer suggested retail price (USD) |

### `fact_inventory` — DC on-hand and in-transit
Grain: product × site × week.
| column | type | meaning |
|---|---|---|
| `product_id`, `site_id`, `week` | keys | |
| `on_hand` | int | Units on hand at the site |
| `in_transit` | int | Units inbound to the site |

### `fact_forecast` — demand forecast snapshots
Grain: snapshot × product × customer × site × week. Twelve snapshots (vintages), each with a
13-week horizon.
| column | type | meaning |
|---|---|---|
| `snapshot_date` | date | When the forecast was generated |
| `product_id`, `customer_id`, `site_id`, `week` | keys | The forecasted week |
| `baseline_qty` | int | Statistical baseline forecast |
| `promo_uplift_qty` | int | Forecast uplift attributed to promotions (`0` in this dataset) |
| `final_forecast_qty` | int | `baseline_qty + promo_uplift_qty` |
| `actual_qty` | float | Realized units for that week (blank for weeks still in the future) |

Example: `2025-07-28, NWO-1001, CUST_MEGA, DC_SOUTH, 2025-08-04, 220, 0, 220, 199.0`
