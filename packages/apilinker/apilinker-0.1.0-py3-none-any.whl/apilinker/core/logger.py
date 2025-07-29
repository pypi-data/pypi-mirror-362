"""
Logging configuration for ApiLinker.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = None,
    logger_name: str = "apilinker"
) -> logging.Logger:
    """
    Configure and get a logger instance.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file (None for console only)
        logger_name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Get logger
    logger = logging.getLogger(logger_name)
    
    # Clear existing handlers
    if logger.hasHandlers():
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
    
    # Set level
    logger.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log_file is specified
    if log_file:
        # Ensure directory exists
        log_path = Path(log_file)
        log_dir = log_path.parent
        if not log_dir.exists() and str(log_dir) != '.':
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
