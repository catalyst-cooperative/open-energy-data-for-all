import pandas as pd


def load_generation_data(path) -> pd.DataFrame:
    """Load the cleaned Puerto Rico generator operations data from disk."""

    return pd.read_parquet(path)


def yearly_heat_rate_by_energy_source(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate yearly heat rates for each energy source code."""

    fuel_gen_monthly = data.loc[
        data["net_generation_mwh"] > 0,
        [
            "date",
            "energy_source_code",
            "fuel_consumed_for_electricity_mmbtu",
            "net_generation_mwh",
        ],
    ]
    fuel_gen_yearly = fuel_gen_monthly.assign(
        year=fuel_gen_monthly["date"].dt.year
    ).drop(columns="date")
    fleets_yearly = fuel_gen_yearly.groupby(
        by=["year", "energy_source_code"], observed=True
    ).sum()
    yearly_heat_rates = (
        fleets_yearly["fuel_consumed_for_electricity_mmbtu"]
        / fleets_yearly["net_generation_mwh"]
    ).dropna()
    return yearly_heat_rates


if __name__ == "__main__":
    generation_data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(generation_data)
