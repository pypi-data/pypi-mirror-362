"""
Sherlock AI - Your AI assistant package
"""

__version__ = "1.4.1"

# Import main components for easy access
from .performance import log_performance, PerformanceTimer
from .logging_setup import sherlock_ai, get_logger, get_logging_stats, get_current_config, SherlockAI
from .config import LoggingConfig, LoggingPresets, LogFileConfig, LoggerConfig
from .utils import set_request_id, get_request_id, clear_request_id
from .monitoring import (
    monitor_memory,
    monitor_resources,
    MemoryTracker,
    ResourceTracker,
    ResourceMonitor,
)
from .analysis import hardcoded_value_detector, CodeAnalyzer

# ✅ Logger name constants 
class LoggerNames:
    """Available logger names for use with get_logger()"""
    API = "ApiLogger"
    DATABASE = "DatabaseLogger"
    SERVICES = "ServiceLogger"
    PERFORMANCE = "PerformanceLogger"
    MONITORING = "MonitoringLogger"

# ✅ Convenience function
def list_available_loggers():
    """Get list of all available logger names"""
    return [
        LoggerNames.API,
        LoggerNames.DATABASE,
        LoggerNames.SERVICES,
        LoggerNames.PERFORMANCE,
        LoggerNames.MONITORING
    ]

__all__ = [
    # Performance Logging
    "log_performance", 
    "PerformanceTimer",

    # Memory and Resource Monitoring
    "monitor_memory",
    "monitor_resources",
    "MemoryTracker",
    "ResourceTracker",
    "ResourceMonitor",

    # Logging Configuration
    "SherlockAI",
    "sherlock_ai",
    "get_logger",
    "get_logging_stats",
    "get_current_config",
    "LoggingConfig",
    "LoggingPresets",
    "LogFileConfig",
    "LoggerConfig",

    # Request ID
    "set_request_id",
    "get_request_id",
    "clear_request_id",
    
    # Logger utilities
    "LoggerNames",
    "list_available_loggers",

    # Analysis
    "hardcoded_value_detector",
    "CodeAnalyzer",

    # Package info
    "__version__",
]