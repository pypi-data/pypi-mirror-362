"""Singleton python based logging and execution logging decorator."""

import functools
import logging
import threading
import time
from typing import Any, Callable, Optional, TypeVar, cast

from configs.config import settings

T = TypeVar("T", bound=Callable[..., Any])


class AppLogger:
    """Singleton logging class using Dynaconf settings.

    This class configures and provides a singleton logger instance
    that uses settings from a Dynaconf configuration.

    Args:
        logger_name (Optional[str]): Optional name for the logger.

    Attributes:
        _instance (Optional[AppLogger]): The singleton instance of the logger.
        _lock (threading.Lock): A lock to ensure thread-safe instantiation.
        _initialized (bool): Flag indicating if the logger has been initialized.
    """

    _instance: Optional["AppLogger"] = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls, logger_name: Optional[str] = None) -> "AppLogger":
        """Create or return the singleton instance.

        Args:
            logger_name (Optional[str]): Optional name for the logger.

        Returns:
            AppLogger: The singleton logger instance.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AppLogger, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, logger_name: Optional[str] = None) -> None:  # noqa: D107
        if self._initialized:
            return
        self._initialized = True

        self.settings = settings
        self.logger_name = logger_name or self.settings.get("app_name", "MyApp")
        self.logger = logging.getLogger(self.logger_name)
        self._configure_logger()

    def _configure_logger(self) -> None:
        """Configure the logger based on settings.

        Returns:
            None: This doesn't return anything meaningful.
        """
        log_level = getattr(logging, self.settings.logging.log_level.upper())
        log_format = self.settings.logging.log_format

        self.logger.handlers.clear()
        self.logger.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.propagate = False

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger.
        """
        return self.logger

    def debug(self, message: str) -> None:
        """Log a debug message.

        Args:
            message (str): The message to log.

        Returns:
            None: This doesn't return anything meaningful.
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message (str): The message to log.

        Returns:
            None: This doesn't return anything meaningful.
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message.

        Args:
            message (str): The message to log.

        Returns:
            None: This doesn't return anything meaningful.
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message (str): The message to log.

        Returns:
            None: This doesn't return anything meaningful.
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical message.

        Args:
            message (str): The message to log.

        Returns:
            None: This doesn't return anything meaningful.
        """
        self.logger.critical(message)


def log_execution(func: T) -> T:
    """Decorator that logs execution details of a function or method.

    This includes entry, arguments, return value, execution time,
    and exceptions if any occur during execution.

    Args:
        func (T): The function or method to be wrapped.

    Returns:
        T: The wrapped function with logging.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger: logging.Logger = AppLogger().get_logger()
        func_name: str = func.__name__

        is_bound_method: bool = bool(
            args
            and (
                isinstance(args[0], object)
                and hasattr(args[0], "__class__")
                and hasattr(args[0].__class__, func_name)
            )
        )

        full_name: str = (
            f"{args[0].__class__.__name__}.{func_name}"
            if is_bound_method
            else func_name
        )

        logger.info(f"Entering: {full_name}")
        logger.debug(f"Args: {args}, kwargs: {kwargs}")

        start_time: float = time.time()
        result: Any  # Declare here to satisfy type checker
        duration: float

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{full_name} failed in {duration:.4f}s: {e}")
            logger.debug(f"Exception: {type(e).__name__}: {e}")
            raise
        else:
            duration = time.time() - start_time
            logger.info(f"{full_name} completed in {duration:.4f}s")
            logger.debug(f"Return: {result}")
            return result
        finally:
            logger.debug(f"Exiting: {full_name}")

    return cast(T, wrapper)
