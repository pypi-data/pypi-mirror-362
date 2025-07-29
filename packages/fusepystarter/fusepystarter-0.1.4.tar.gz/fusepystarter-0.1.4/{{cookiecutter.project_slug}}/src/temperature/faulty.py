"""Temperature Conversion Module with Intentional Errors for Testing."""

from configs.config import settings
from src.decorators import log_execution, logger
from src.temperature.advanced import TemperatureConverter


class FaultyTemperatureConverter(TemperatureConverter):
    """A converter that intentionally introduces errors for testing purposes.

    Attributes:
        calibration_error: An intentional error offset to apply to conversions.
    """

    calibration_error = 0  # fallback

    @classmethod
    def init_settings(cls) -> None:
        """Initialize converter settings by loading calibration error from config.

        Returns:
            None: This method doesn't return anything meaningful.
        """
        cls.calibration_error = settings.get("calibration_error", 0)
        logger.info(f"Calibration error loaded: {cls.calibration_error}")

    @classmethod
    @log_execution
    def convert(cls, temp: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between units with intentional errors.

        Args:
            temp (float): Temperature value to convert.
            from_unit (str): Original temperature unit (case-sensitive).
            to_unit (str): Target temperature unit (case-sensitive).

        Returns:
            float: Converted temperature value with intentional errors.
        """
        cls.init_settings()  # Ensure settings are loaded
        result = super().convert(temp, from_unit, to_unit)

        if from_unit == "C" and to_unit == "F":
            logger.debug(
                f"Applying calibration error: -{cls.calibration_error}° to C→F"
            )
            return result - cls.calibration_error

        elif from_unit == "F" and to_unit == "C":
            logger.debug("Applying intentional multiplier 1.1 to F→C")
            return result * 1.1

        elif "K" in (from_unit, to_unit):
            logger.debug("Applying fixed offset +2.5 to Kelvin-related conversion")
            return result + 2.5

        logger.warning(
            f"No intentional error rule matched for: {from_unit} → {to_unit}"
        )
        return round(result)
