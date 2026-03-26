from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import (
    load_generation_data,
    yearly_heat_rate_by_energy_source,
)


def test_load_generation_data_returns_expected_columns():
    data = load_generation_data()

    assert not data.empty
    assert {
        "plant_id_eia",
        "plant_name_eia",
        "energy_source_code",
        "fuel_consumed_mmbtu",
        "net_generation_mwh",
        "date",
    }.issubset(data.columns)


def test_yearly_heat_rate_shows_solar_reporting_change():
    data = load_generation_data()

    heat_rates = yearly_heat_rate_by_energy_source(data)
    solar_heat_rates = heat_rates.loc[
        heat_rates["energy_source_code"] == "solar"
    ].set_index("year")["heat_rate_mmbtu_per_mwh"]
    wind_heat_rates = heat_rates.loc[
        heat_rates["energy_source_code"] == "wind"
    ].set_index("year")["heat_rate_mmbtu_per_mwh"]

    assert 8.0 < solar_heat_rates.loc[2021] < 10.0
    assert solar_heat_rates.loc[2023] == pytest.approx(3.412, abs=0.01)
    assert wind_heat_rates.loc[2023] == pytest.approx(3.412, abs=0.01)


def test_yearly_heat_rate_uses_ratio_of_totals_not_mean_of_row_heat_rates():
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-06-01",
                ]
            ),
            "energy_source_code": ["natural_gas", "natural_gas", "solar"],
            "fuel_consumed_mmbtu": [1_000.0, 10.0, 150.0],
            "net_generation_mwh": [100.0, 10.0, 30.0],
        }
    )

    heat_rates = yearly_heat_rate_by_energy_source(data)
    natural_gas_2024 = heat_rates.loc[
        (heat_rates["year"] == 2024)
        & (heat_rates["energy_source_code"] == "natural_gas"),
        "heat_rate_mmbtu_per_mwh",
    ].iloc[0]

    assert natural_gas_2024 == pytest.approx(9.1818181818)
