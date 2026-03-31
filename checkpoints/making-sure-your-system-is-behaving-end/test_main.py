from main import (
    load_generation_data,
    yearly_heat_rate_by_energy_source,
)


def test_heat_rates_exist():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert not heat_rates.empty, "Heat rates should be non-empty series."


def test_heat_rates_sensible_values():
    data = load_generation_data("data/pr_gen_fuel_monthly.parquet")
    heat_rates = yearly_heat_rate_by_energy_source(data)
    assert (heat_rates >= 0).all()
    assert (heat_rates <= 15).all()
