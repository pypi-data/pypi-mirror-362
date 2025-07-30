"""
loguru_config.py
"""
import sys
from dataclasses import dataclass


@dataclass
class LoguruConfig:
    """Configuration for LoggerWrapper behavior."""
    format_string: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[module_name]}:{extra[caller_name]}</cyan>:"
        "<cyan>{extra[caller_line]}</cyan> | "
        "<level>{message}</level>"
    )
    default_level: str = "DEBUG"
    enable_lazy: bool = True
    sink = sys.stderr
