import pandas as pd


def load_generation_data(path) -> pd.DataFrame:
    """Load the cleaned Puerto Rico generator operations data from disk."""

    return pd.read_parquet(path)


def yearly_heat_rate_by_energy_source(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate heat rates for each year, across every energy source code.

    We want to know how much efficiently Puerto Rico generates electricity from
    each fuel source.
    """

    fuel_gen_monthly = data.loc[
        data["net_generation_mwh"] > 0,
        [
            "date",
            "energy_source_code",
            "fuel_consumed_for_electricity_mmbtu",
            "net_generation_mwh",
        ],
    ]
    monthly_heat_rates = fuel_gen_monthly.assign(
        year=fuel_gen_monthly["date"].dt.year,
        heat_rate_mmbtu_per_mwh=fuel_gen_monthly["fuel_consumed_for_electricity_mmbtu"]
        / fuel_gen_monthly["net_generation_mwh"],
    )
    yearly_heat_rates = (
        monthly_heat_rates.groupby(["year", "energy_source_code"], observed=False)[
            "heat_rate_mmbtu_per_mwh"
        ]
        .mean()
        .dropna()
    )
    return yearly_heat_rates


if __name__ == "__main__":
    generation_data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(generation_data)
