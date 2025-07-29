import pytest

import src
from src.temperature import FaultyTemperatureConverter as Converter


class TestFaultyTemperatureConverter:
    @staticmethod
    def test_c_to_f():
        Converter.init_settings()
        expected = (0 * 9 / 5 + 32) - Converter.calibration_error
        assert Converter.convert(0, "C", "F") == pytest.approx(expected)

    @staticmethod
    def test_f_to_c():
        expected = ((212 - 32) * 5 / 9) * 1.1
        assert Converter.convert(212, "F", "C") == pytest.approx(expected)

    @staticmethod
    def test_k_related_conversion():
        src.ENV = "prod"
        expected = 273.15 + 2.5
        assert Converter.convert(0, "C", "K") == pytest.approx(expected)

    @staticmethod
    def test_invalid_unit():
        with pytest.raises(ValueError):
            Converter.convert(100, "X", "C")

    @staticmethod
    def test_same_unit():
        assert Converter.convert(42.0, "C", "C") == 42.0
