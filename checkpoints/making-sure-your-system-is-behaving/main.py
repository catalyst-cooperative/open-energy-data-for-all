from pathlib import Path

import pandas as pd


def load_generation_data(path: str | Path = "data/pr_gen_fuel_monthly.parquet") -> pd.DataFrame:
    """Load the cleaned Puerto Rico generator operations data from disk.

    Callers get a pandas DataFrame with one row per plant, fuel, and month.
    The intent is to keep file I/O isolated in one place so tests can either
    exercise the real dataset or swap in small in-memory DataFrames for the
    analysis logic.
    """

    return pd.read_parquet(path)


def yearly_heat_rate_by_energy_source(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate yearly heat rates for each energy source code.

    Callers get one row per year and energy source with a `heat_rate_mmbtu_per_mwh`
    column. The intent is to provide a small analysis function that is easy to
    test, while still looking like the kind of grouped calculation people make
    on real energy data.
    """

    data_with_generation = data.loc[data["net_generation_mwh"] > 0].copy()
    data_with_generation["year"] = data_with_generation["date"].dt.year
    data_with_generation["heat_rate_mmbtu_per_mwh"] = (
        data_with_generation["fuel_consumed_mmbtu"]
        / data_with_generation["net_generation_mwh"]
    )

    yearly_heat_rates = (
        data_with_generation.groupby(["year", "energy_source_code"], observed=True)[
            "heat_rate_mmbtu_per_mwh"
        ]
        .mean()
        .reset_index()
        .sort_values(["year", "energy_source_code"])
        .reset_index(drop=True)
    )
    return yearly_heat_rates


if __name__ == "__main__":
    generation_data = load_generation_data()
    heat_rates = yearly_heat_rate_by_energy_source(generation_data)
    print(heat_rates.tail(12).to_string(index=False))
