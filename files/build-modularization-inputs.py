"""This script dirties the existing PR monthly generation data to provide additional
things for students to handle when modularizing fixes."""

import pandas as pd
import numpy as np

pr_gen_fuel = pd.read_parquet("data/raw_eia923__puerto_rico_generation_fuel.parquet")

# Handle EIA null values
pr_gen_fuel = pr_gen_fuel.replace(to_replace = ".", value = pd.NA)

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

#### monthly pivoting
def melt_monthly_vars(pr_gen_fuel: pd.DataFrame, melted_var: str) -> pd.DataFrame:
    # set up shared index
    index_cols = ["plant_id_eia", "plant_name_eia", "report_year", "prime_mover_code", "energy_source_code", "fuel_unit"]

    var_cols = index_cols + [col for col in pr_gen_fuel.columns if col.startswith(melted_var)]
    var_df = pr_gen_fuel.loc[:, var_cols]

    ## Melt the fuel_consumed columns
    var_melt = var_df.melt(
        id_vars=index_cols,
        var_name="month",
        value_name=melted_var
    )
    var_melt["month"] = var_melt["month"].str.replace(f"{melted_var}_", "")
    var_melt = var_melt.set_index(index_cols + ["month"])
    return var_melt


fuel_elec_mmbtu_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_for_electricity_mmbtu")
fuel_elec_units_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_for_electricity_units")
fuel_mmbtu_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_mmbtu")
fuel_units_melt = melt_monthly_vars(pr_gen_fuel, "fuel_consumed_units_mmbtu")
net_gen_melt = melt_monthly_vars(pr_gen_fuel, "net_generation_mwh")

pr_gen_fuel_melt = pd.concat(
    [fuel_elec_mmbtu_melt, fuel_elec_units_melt, fuel_mmbtu_melt, fuel_units_melt, net_gen_melt],
    axis="columns",
).reset_index()

## Create date from month and year
pr_gen_fuel_melt["date"] = pd.to_datetime(
    pr_gen_fuel_melt["month"] + pr_gen_fuel_melt["report_year"].astype(int).astype(str),
    format="%B%Y",
)
## Drop old date columns
pr_gen_fuel_melt = pr_gen_fuel_melt.drop(columns = ["report_year", "month"])

# Introduce units problem
thousands_index = pr_gen_fuel_melt[pr_gen_fuel_melt.fuel_unit.isin(['barrels', 'short tons'])].sample(100, random_state= 123).index
pr_gen_fuel_melt.loc[thousands_index] = pr_gen_fuel_melt.loc[thousands_index].replace({'short tons': 'thousand short tons', 'barrels': 'thousand barrels'})

pr_gen_fuel_melt.dtypes
pr_gen_fuel_melt.loc[thousands_index, [col for col in pr_gen_fuel_melt.columns if col.endswith('_units')]] = pr_gen_fuel_melt.loc[thousands_index, [col for col in pr_gen_fuel_melt.columns if col.endswith('_units')]].astype(float) * 1000

#Introduce one more bad row
extra_row = pr_gen_fuel_melt[(pr_gen_fuel_melt.plant_id_eia == 61082)&(pr_gen_fuel_melt.date == '2023-04-01')&(pr_gen_fuel_melt.fuel_unit == "barrels")].copy()
extra_row.loc[:, 'fuel_consumed_for_electricity_mmbtu'] = pd.NA
pr_gen_fuel_melt = pd.concat([pr_gen_fuel_melt, extra_row]).sort_values(['date'])

# Write out to DB
pr_gen_fuel_melt.to_parquet("data/modularization/pr_gen_fuel_monthly.parquet")
