import pytest

from src.temperature import celsius_to_fahrenheit, fahrenheit_to_celsius


@pytest.mark.parametrize(
    "celsius, expected_fahrenheit",
    [
        (0, 32.0),  # Freezing point
        (100, 212.0),  # Boiling point
        (-40, -40.0),  # Same in both scales
        (37, 98.6),  # Human body temperature
        (25.5, 77.9),  # Arbitrary float
    ],
)
def test_celsius_to_fahrenheit(celsius, expected_fahrenheit):
    result = celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(expected_fahrenheit)


@pytest.mark.parametrize(
    "fahrenheit, expected_celsius",
    [
        (32, 0.0),  # Freezing point
        (212, 100.0),  # Boiling point
        (-40, -40.0),  # Same in both scales
        (98.6, 37.0),  # Human body temperature
        (77.9, 25.5),  # Arbitrary float
    ],
)
def test_fahrenheit_to_celsius(fahrenheit, expected_celsius):
    result = fahrenheit_to_celsius(fahrenheit)
    assert result == pytest.approx(expected_celsius)
