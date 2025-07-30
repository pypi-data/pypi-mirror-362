import warnings

import pytest

import src
from src.temperature import TemperatureConverter


class TestTemperatureConverter:
    @staticmethod
    @pytest.mark.parametrize(
        "temp, from_unit, to_unit, expected",
        [
            (0, "C", "F", 32.0),
            (100, "C", "K", 373.15),
            (32, "F", "C", 0.0),
            (212, "F", "K", 373.15),
            (273.15, "K", "C", 0.0),
            (0, "K", "F", -459.67),
        ],
    )
    def test_valid_conversions(temp, from_unit, to_unit, expected):
        result = TemperatureConverter.convert(temp, from_unit, to_unit)
        assert result == pytest.approx(expected)

    @staticmethod
    def test_same_unit_returns_input():
        assert TemperatureConverter.convert(42, "C", "C") == 42

    @staticmethod
    @pytest.mark.parametrize(
        "from_unit, to_unit",
        [("X", "C"), ("C", "Y"), ("A", "B"), ("", "C"), ("K", "Kelvin")],
    )
    def test_invalid_units_raise(from_unit, to_unit):
        with pytest.raises(ValueError, match="Invalid temperature unit"):
            TemperatureConverter.convert(100, from_unit, to_unit)

    @staticmethod
    def test_kelvin_warning_in_prod(monkeypatch):
        monkeypatch.setattr(src, "ENV", "prod")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = TemperatureConverter.convert(0, "C", "K")
            assert result == pytest.approx(273.15)

            # Confirm warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, RuntimeWarning)
            assert "Kelvin conversions are experimental" in str(w[0].message)

    @staticmethod
    def test_no_kelvin_warning_in_dev(monkeypatch):
        monkeypatch.setattr(src, "ENV", "dev")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = TemperatureConverter.convert(0, "C", "K")
            assert result == pytest.approx(273.15)
            assert len(w) == 0
