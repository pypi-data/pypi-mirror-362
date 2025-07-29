"""Temperature conversion functions between Celsius and Fahrenheit."""

from src.decorators import log_execution, logger


@log_execution
def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit.

    Args:
        c (float): Temperature in Celsius

    Returns:
        float: Temperature in Fahrenheit
    """
    if c == 0:
        logger.debug("Celsius input is freezing point.")
    elif c == 100:
        logger.debug("Celsius input is boiling point.")

    result = (c * 9 / 5) + 32
    logger.debug(f"Converted {c}°C to {result}°F")
    return result


@log_execution
def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius.

    Args:
        f (float): Temperature in Fahrenheit

    Returns:
        float: Temperature in Celsius
    """
    if f == 32:
        logger.debug("Fahrenheit input is freezing point.")
    elif f == 212:
        logger.debug("Fahrenheit input is boiling point.")

    result = (f - 32) * 5 / 9
    logger.debug(f"Converted {f}°F to {result}°C")
    return result
