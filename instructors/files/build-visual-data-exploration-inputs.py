import pandas as pd
import numpy as np

pr_gen_fuel = pd.read_parquet("data/raw_eia923__puerto_rico_generation_fuel.parquet")

# Handle EIA null values
pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA)

# Silence some warnings about deprecated Pandas behavior
pd.set_option("future.no_silent_downcasting", True)

# Convert data types (mmbtu/units to numeric, booleans, categories)
pr_gen_fuel = pr_gen_fuel.convert_dtypes()
for colname in pr_gen_fuel.columns:
    if (
        "fuel_consumption" in colname
        or "fuel_consumed" in colname
        or "net_generation" in colname
        or "fuel_mmbtu_per_unit" in colname
    ):
        pr_gen_fuel[colname] = pr_gen_fuel[colname].astype("float64")


pr_gen_fuel["associated_combined_heat_power"] = (
    pr_gen_fuel["associated_combined_heat_power"]
    .astype("object") # necessary for the types to work for the .replace() call
    .replace({"Y": True, "N": False})
    .astype("boolean")
)
pr_gen_fuel = pr_gen_fuel.astype({
    "energy_source_code": "category",
    "fuel_type_code_agg": "category",
    "prime_mover_code": "category",
    "reporting_frequency_code": "category",
    "data_maturity": "category",
    "plant_state": "category",
    "fuel_unit": "category",
})

#### monthly pivoting

# set up shared index
index_cols = ["plant_id_eia", "plant_name_eia", "report_year", "prime_mover_code", "energy_source_code", "fuel_unit"]

# Pivot fuel_consumed_for_electricity MMBTU columns

fuel_elec_mmbtu_cols = index_cols + [col for col in pr_gen_fuel.columns if "fuel_consumed_for_electricity_mmbtu" in col]
fuel_elec_mmbtu = pr_gen_fuel.loc[:, fuel_elec_mmbtu_cols]

## Melt the fuel_consumed columns
fuel_elec_mmbtu_melt = fuel_elec_mmbtu.melt(
    id_vars=index_cols,
    var_name="month",
    value_name="fuel_consumed_for_electricity_mmbtu"
)
fuel_elec_mmbtu_melt["month"] = fuel_elec_mmbtu_melt["month"].str.replace("fuel_consumed_for_electricity_mmbtu_", "")
fuel_elec_mmbtu_melt = fuel_elec_mmbtu_melt.set_index(index_cols + ["month"])

# Pivot fuel_consumed_for_electricity UNITS columns
fuel_elec_units_cols = index_cols + [col for col in pr_gen_fuel.columns if "fuel_consumed_for_electricity_units" in col]
fuel_elec_units = pr_gen_fuel.loc[:, fuel_elec_units_cols]

## Melt the fuel_consumed columns
fuel_elec_units_melt = fuel_elec_units.melt(
    id_vars=index_cols,
    var_name="month",
    value_name="fuel_consumed_for_electricity_units"
)
fuel_elec_units_melt["month"] = fuel_elec_units_melt["month"].str.replace("fuel_consumed_for_electricity_units_", "")
fuel_elec_units_melt = fuel_elec_units_melt.set_index(index_cols + ["month"])

# Pivot fuel_consumed MMBTU columns

fuel_mmbtu_cols = index_cols + [col for col in pr_gen_fuel.columns if "fuel_consumed_mmbtu" in col]
fuel_mmbtu = pr_gen_fuel.loc[:, fuel_mmbtu_cols]

## Melt the fuel_consumed columns
fuel_mmbtu_melt = fuel_mmbtu.melt(
    id_vars=index_cols,
    var_name="month",
    value_name="fuel_consumed_mmbtu"
)
fuel_mmbtu_melt["month"] = fuel_mmbtu_melt["month"].str.replace("fuel_consumed_mmbtu_", "")
fuel_mmbtu_melt = fuel_mmbtu_melt.set_index(index_cols + ["month"])

# Pivot fuel_consumed UNITS columns

fuel_units_cols = index_cols + [col for col in pr_gen_fuel.columns if "fuel_consumed_units" in col]
fuel_units = pr_gen_fuel.loc[:, fuel_units_cols]

## Melt the fuel_consumed columns
fuel_units_melt = fuel_units.melt(
    id_vars=index_cols,
    var_name="month",
    value_name="fuel_consumed_units"
)
fuel_units_melt["month"] = fuel_units_melt["month"].str.replace("fuel_consumed_units_", "")
fuel_units_melt = fuel_units_melt.set_index(index_cols + ["month"])

# Pivot net_generation columns

net_gen_cols = index_cols + [col for col in pr_gen_fuel.columns if col.startswith("net_generation_mwh")]
net_gen = pr_gen_fuel.loc[:, net_gen_cols]

## Melt the fuel_consumed columns
net_gen_melt = net_gen.melt(
    id_vars=index_cols,
    var_name="month",
    value_name="net_generation_mwh"
)
net_gen_melt["month"] = net_gen_melt["month"].str.replace("net_generation_mwh_", "")
net_gen_melt = net_gen_melt.set_index(index_cols + ["month"])
net_gen_meltpr_gen_fuel_melt = pd.concat(
    [fuel_elec_mmbtu_melt, fuel_elec_units_melt, fuel_mmbtu_melt, fuel_units_melt, net_gen_melt],
    axis="columns",
).reset_index()

pr_gen_fuel_melt = pd.concat(
    [fuel_elec_mmbtu_melt, fuel_elec_units_melt, fuel_mmbtu_melt, fuel_units_melt, net_gen_melt],
    axis="columns",
).reset_index()

## Create date from month and year
pr_gen_fuel_melt["date"] = pd.to_datetime(
    pr_gen_fuel_melt["month"] + pr_gen_fuel_melt["report_year"].astype(str),
    format="%B%Y",
)
## Drop old date columns
pr_gen_fuel_clean = pr_gen_fuel_melt.drop(columns = ["report_year", "month"])

# Plant 62410 has two 2020 data entries but one is null
# Drop the bad row
pr_gen_fuel_final = pr_gen_fuel_clean.loc[
    ~((pr_gen_fuel_clean.plant_id_eia == 62410)
    & (pr_gen_fuel_clean.date.dt.year == 2020)
    & (pr_gen_fuel_clean.fuel_consumed_for_electricity_mmbtu.isnull()))
]

# drop after 2025-03-01 (for now) as these values should not exist
pr_gen_fuel_final = pr_gen_fuel_final.loc[pr_gen_fuel_clean.date < pd.Timestamp("2025-03-01")]

### make a list of all the monthly columns
import calendar
monthly_columns = []
for col in pr_gen_fuel.columns:
    for month in calendar.Month:
        if col.endswith(month.name.lower()):
            monthly_columns.append(col)

### annual table
pr_gen_fuel_annual = pr_gen_fuel.drop(columns=monthly_columns)
### output
pr_gen_fuel_final.to_parquet("data/pr_gen_fuel_monthly.parquet")
pr_gen_fuel_annual.to_parquet("data/pr_gen_fuel_annual.parquet")
