import pytest

from main import (
    load_generation_data,
    yearly_heat_rate_by_energy_source,
)


@pytest.fixture
def pr_data():
    return load_generation_data("data/pr_gen_fuel_monthly.parquet")


@pytest.fixture
def heat_rates(pr_data):
    return yearly_heat_rate_by_energy_source(pr_data)


def test_data_exists(pr_data):
    assert not pr_data.empty


def test_heat_rates_exist(heat_rates):
    assert not heat_rates.empty, "Heat rates should be non-empty series."


def test_heat_rates_sensible_values(heat_rates):
    assert (heat_rates >= 0).all()
    assert (heat_rates <= 15).all()
