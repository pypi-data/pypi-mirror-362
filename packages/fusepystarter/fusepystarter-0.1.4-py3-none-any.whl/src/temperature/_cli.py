"""Temperature conversion CLI interface."""

import fire

from src.decorators import log_execution, logger
from src.temperature import (
    FaultyTemperatureConverter,
    TemperatureConverter,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
)


class Main:
    """Temperature conversion CLI interface.

    Initializes with temperature conversion methods:
    - celsius_to_fahrenheit: Convert Celsius to Fahrenheit
    - fahrenheit_to_celsius: Convert Fahrenheit to Celsius
    - faulty_temp: Faulty temperature converter (for testing)
    - advance_temp: Advanced temperature converter
    """

    def __init__(self) -> None:  # noqa: D107
        logger.info("Initializing CLI commands in Main class.")
        self.celsius_to_fahrenheit = celsius_to_fahrenheit
        self.fahrenheit_to_celsius = fahrenheit_to_celsius
        self.faulty_temp = FaultyTemperatureConverter
        self.advance_temp = TemperatureConverter


@log_execution
def main() -> None:
    """Run the CLI using Fire.

    Returns:
        None: This function does not return a value.
    """
    logger.info("Starting Temperature Conversion CLI...")
    fire.Fire(Main)
