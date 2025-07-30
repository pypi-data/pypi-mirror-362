"""
Logging utilities for ABgrouponline.

This module provides logging configuration and utility functions
for consistent logging across the package.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Union
from .config import get_config

def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
    log_to_file: Optional[bool] = None,
    log_dir: Optional[str] = None,
    max_file_size: Optional[int] = None,
    backup_count: Optional[int] = None
) -> None:
    """
    Setup logging configuration for ABgrouponline.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Log message format string
        log_to_file: Whether to log to file
        log_dir: Directory for log files
        max_file_size: Maximum size of log files in bytes
        backup_count: Number of backup log files to keep
    """
    config = get_config()
    
    # Use config values if not provided
    level = level or config.logging.level
    format_string = format_string or config.logging.format
    log_to_file = log_to_file if log_to_file is not None else config.logging.file_logging
    log_dir = log_dir or config.logging.log_dir
    max_file_size = max_file_size or config.logging.max_file_size
    backup_count = backup_count or config.logging.backup_count
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if log_to_file:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        log_file = log_path / "abgrouponline.log"
        
        # Use rotating file handler to manage log file size
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    
    # Suppress sklearn warnings in logs
    logging.getLogger('sklearn').setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

def set_log_level(level: Union[str, int]) -> None:
    """
    Set the logging level for all ABgrouponline loggers.
    
    Args:
        level: Logging level (string or integer)
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    
    # Set level for root logger
    logging.getLogger().setLevel(level)
    
    # Set level for package loggers
    for name in ['abgrouponline', 'abgrouponline.core', 'abgrouponline.healthcare',
                 'abgrouponline.brain_imaging', 'abgrouponline.language_models',
                 'abgrouponline.forecasting']:
        logging.getLogger(name).setLevel(level)

def disable_warnings() -> None:
    """Disable warning messages from third-party libraries."""
    import warnings
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)
    warnings.filterwarnings('ignore', category=DeprecationWarning)

def enable_debug_mode() -> None:
    """Enable debug mode with verbose logging."""
    set_log_level('DEBUG')
    
    # Enable logging for third-party libraries in debug mode
    logging.getLogger('sklearn').setLevel(logging.INFO)
    logging.getLogger('matplotlib').setLevel(logging.INFO)

def log_function_call(func):
    """
    Decorator to log function calls.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {e}")
            raise
    
    return wrapper

def log_performance(func):
    """
    Decorator to log function performance.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    
    return wrapper

class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__module__)
    
    def log_info(self, message: str, *args, **kwargs):
        """Log info message."""
        self.logger.info(message, *args, **kwargs)
    
    def log_debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(message, *args, **kwargs)
    
    def log_warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(message, *args, **kwargs)
    
    def log_error(self, message: str, *args, **kwargs):
        """Log error message."""
        self.logger.error(message, *args, **kwargs) 