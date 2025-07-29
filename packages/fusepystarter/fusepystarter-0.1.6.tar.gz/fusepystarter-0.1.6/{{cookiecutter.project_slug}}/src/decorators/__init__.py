"""Initialize decorators package and expose public logging utilities."""

from src.decorators.logging_service import AppLogger, log_execution

app_logger = AppLogger()
logger = app_logger.get_logger()

__all__ = ["logger", "log_execution"]
