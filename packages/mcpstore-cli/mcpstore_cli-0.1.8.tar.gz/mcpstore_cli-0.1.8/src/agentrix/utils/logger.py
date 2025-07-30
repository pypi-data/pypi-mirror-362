"""Logging utilities for Agentrix."""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from ..models.config import LoggingConfig

# Global logger registry
_loggers = {}
_configured = False


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    if name not in _loggers:
        logger = logging.getLogger(f"agentrix.{name}")
        _loggers[name] = logger
    
    return _loggers[name]


def setup_logging(config: LoggingConfig) -> None:
    """Set up logging configuration."""
    global _configured
    
    if _configured:
        return
    
    # Configure root logger
    root_logger = logging.getLogger("agentrix")
    root_logger.setLevel(getattr(logging, config.level.value))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with Rich
    if config.console_enabled:
        console = Console(stderr=True)
        console_handler = RichHandler(
            console=console,
            show_time=True,
            show_path=True,
            markup=True,
            rich_tracebacks=True,
            tracebacks_show_locals=config.level.value == "DEBUG",
        )
        console_handler.setLevel(getattr(logging, config.level.value))
        
        # Custom formatter for Rich handler
        formatter = logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]"
        )
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handler
    if config.log_file:
        log_file = Path(config.log_file).expanduser().resolve()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Use RotatingFileHandler for log rotation
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=config.max_file_size,
            backupCount=config.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, config.level.value))
        
        # File formatter
        file_formatter = logging.Formatter(
            fmt=config.format,
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    root_logger.propagate = False
    
    # Configure third-party loggers
    _configure_third_party_loggers(config)
    
    _configured = True


def _configure_third_party_loggers(config: LoggingConfig) -> None:
    """Configure logging for third-party libraries."""
    # Reduce noise from HTTP libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    # Rich library
    logging.getLogger("rich").setLevel(logging.WARNING)
    
    # Only show DEBUG for our own modules in debug mode
    if config.level.value != "DEBUG":
        logging.getLogger("asyncio").setLevel(logging.WARNING)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        module_name = self.__class__.__module__.replace("agentrix.", "")
        class_name = self.__class__.__name__
        return get_logger(f"{module_name}.{class_name}")


def log_function_call(func_name: str, args: dict, result: Optional[str] = None):
    """Log a function call with arguments and result."""
    logger = get_logger("function_calls")
    
    # Format arguments
    args_str = ", ".join(f"{k}={v}" for k, v in args.items() if v is not None)
    
    if result:
        logger.debug(f"{func_name}({args_str}) -> {result}")
    else:
        logger.debug(f"{func_name}({args_str})")


def log_performance(operation: str, duration: float, details: Optional[dict] = None):
    """Log performance metrics."""
    logger = get_logger("performance")
    
    message = f"{operation} completed in {duration:.3f}s"
    if details:
        details_str = ", ".join(f"{k}={v}" for k, v in details.items())
        message += f" ({details_str})"
    
    logger.info(message)


def log_error_with_context(error: Exception, context: dict):
    """Log an error with additional context."""
    logger = get_logger("errors")
    
    context_str = ", ".join(f"{k}={v}" for k, v in context.items())
    logger.error(f"{type(error).__name__}: {error} (Context: {context_str})")


def create_debug_logger(name: str) -> logging.Logger:
    """Create a debug logger that always logs to console."""
    logger = logging.getLogger(f"agentrix.debug.{name}")
    
    if not logger.handlers:
        console = Console(stderr=True)
        handler = RichHandler(
            console=console,
            show_time=True,
            show_path=True,
            markup=True,
            rich_tracebacks=True,
        )
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            fmt="[DEBUG] %(message)s",
            datefmt="[%X]"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    
    return logger 