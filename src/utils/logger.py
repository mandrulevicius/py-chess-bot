"""Structured logging configuration for PyChessBot."""

import logging
import sys
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        
        # Format the message
        formatted = super().format(record)
        
        # Reset levelname for future use
        record.levelname = levelname
        
        return formatted


def get_logger(name: str = __name__, level: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Don't add handlers if already configured
    if logger.handlers:
        return logger
    
    # Set level
    if level:
        logger.setLevel(getattr(logging, level.upper()))
    else:
        logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


def get_game_logger() -> logging.Logger:
    """Get logger for game-related events."""
    return get_logger('pychessbot.game')


def get_ui_logger() -> logging.Logger:
    """Get logger for UI-related events."""
    return get_logger('pychessbot.ui')


def get_ai_logger() -> logging.Logger:
    """Get logger for AI-related events."""
    return get_logger('pychessbot.ai')


def get_main_logger() -> logging.Logger:
    """Get logger for main application events."""
    return get_logger('pychessbot.main')


def configure_logging(level: str = 'INFO', quiet: bool = False, log_file: str = None) -> None:
    """
    Configure logging for the entire application.
    
    Args:
        level: Global log level
        quiet: If True, suppress all logging output
        log_file: Optional file path for logging output
    """
    if quiet:
        logging.disable(logging.CRITICAL)
        return
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler (colored)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_formatter = logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            # Don't fail if we can't create log file, just print warning
            print(f"Warning: Could not create log file {log_file}: {e}")


def disable_external_logging() -> None:
    """Disable logging from external libraries to reduce noise."""
    # Disable pygame logging
    pygame_logger = logging.getLogger('pygame')
    pygame_logger.setLevel(logging.WARNING)
    
    # Disable stockfish logging if it exists
    stockfish_logger = logging.getLogger('stockfish')
    stockfish_logger.setLevel(logging.WARNING)