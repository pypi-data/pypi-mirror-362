"""
Logging utilities for SE-AGI
Provides comprehensive logging setup and management
"""

import logging
import logging.handlers
import sys
import os
from typing import Dict, Optional, Any
from datetime import datetime
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                          'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process', 'getMessage']:
                log_entry[key] = value
        
        return json.dumps(log_entry)


class ContextualLogger:
    """Logger that maintains context across operations"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.context: Dict[str, Any] = {}
    
    def set_context(self, **kwargs):
        """Set context variables"""
        self.context.update(kwargs)
    
    def clear_context(self):
        """Clear all context"""
        self.context.clear()
    
    def _log_with_context(self, level, message, *args, **kwargs):
        """Log message with context"""
        extra = kwargs.pop('extra', {})
        extra.update(self.context)
        kwargs['extra'] = extra
        
        # Get the appropriate logging method
        log_method = getattr(self.logger, level.lower())
        log_method(message, *args, **kwargs)
    
    def debug(self, message, *args, **kwargs):
        self._log_with_context('DEBUG', message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        self._log_with_context('INFO', message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        self._log_with_context('WARNING', message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        self._log_with_context('ERROR', message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        self._log_with_context('CRITICAL', message, *args, **kwargs)


def setup_logging(name: str = "se_agi", 
                 level: str = "INFO",
                 log_dir: Optional[str] = None,
                 enable_console: bool = True,
                 enable_file: bool = True,
                 enable_json: bool = False,
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5,
                 config: Optional[Dict[str, Any]] = None) -> ContextualLogger:
    """
    Setup comprehensive logging for SE-AGI
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (None to disable file logging)
        enable_console: Whether to enable console logging
        enable_file: Whether to enable file logging
        enable_json: Whether to use JSON formatting
        max_file_size: Maximum size of log files before rotation
        backup_count: Number of backup files to keep
        config: Additional configuration options
        
    Returns:
        ContextualLogger instance
    """
    config = config or {}
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    if enable_json:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if enable_file and log_dir:
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Main log file
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Error log file (errors and above only)
        error_log_file = os.path.join(log_dir, f"{name}_errors.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
    
    # Add custom handlers from config
    if 'custom_handlers' in config:
        for handler_config in config['custom_handlers']:
            handler = create_custom_handler(handler_config)
            if handler:
                handler.setFormatter(formatter)
                logger.addHandler(handler)
    
    # Set up root logger to capture all logs
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.setLevel(logging.WARNING)  # Only capture warnings and above from other modules
        if enable_console:
            root_handler = logging.StreamHandler(sys.stdout)
            root_handler.setFormatter(formatter)
            root_logger.addHandler(root_handler)
    
    # Create contextual logger
    contextual_logger = ContextualLogger(logger)
    
    # Log initialization
    contextual_logger.info(f"Logging initialized for {name}")
    contextual_logger.info(f"Log level: {level}")
    if log_dir:
        contextual_logger.info(f"Log directory: {log_dir}")
    
    return contextual_logger


def create_custom_handler(handler_config: Dict[str, Any]) -> Optional[logging.Handler]:
    """Create a custom logging handler from configuration"""
    try:
        handler_type = handler_config.get('type')
        
        if handler_type == 'smtp':
            # Email handler
            from logging.handlers import SMTPHandler
            return SMTPHandler(
                mailhost=handler_config['mailhost'],
                fromaddr=handler_config['fromaddr'],
                toaddrs=handler_config['toaddrs'],
                subject=handler_config.get('subject', 'SE-AGI Log Alert')
            )
        
        elif handler_type == 'syslog':
            # Syslog handler
            from logging.handlers import SysLogHandler
            return SysLogHandler(
                address=handler_config.get('address', '/dev/log'),
                facility=handler_config.get('facility', SysLogHandler.LOG_USER)
            )
        
        elif handler_type == 'webhook':
            # Custom webhook handler (would need implementation)
            # This is a placeholder for webhook logging
            return None
        
        else:
            return None
            
    except Exception as e:
        print(f"Error creating custom handler: {e}")
        return None


class LogCapture:
    """Context manager for capturing logs during testing or analysis"""
    
    def __init__(self, logger_name: str = None, level: str = "DEBUG"):
        self.logger_name = logger_name
        self.level = getattr(logging, level.upper())
        self.records = []
        self.handler = None
        self.original_level = None
    
    def __enter__(self):
        # Create memory handler
        self.handler = logging.handlers.MemoryHandler(capacity=1000)
        self.handler.setLevel(self.level)
        
        # Get logger
        if self.logger_name:
            logger = logging.getLogger(self.logger_name)
        else:
            logger = logging.getLogger()
        
        # Store original level and set new level
        self.original_level = logger.level
        logger.setLevel(self.level)
        
        # Add handler
        logger.addHandler(self.handler)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Get logger
        if self.logger_name:
            logger = logging.getLogger(self.logger_name)
        else:
            logger = logging.getLogger()
        
        # Remove handler
        logger.removeHandler(self.handler)
        
        # Restore original level
        if self.original_level is not None:
            logger.setLevel(self.original_level)
        
        # Store records
        self.records = self.handler.buffer.copy()
        self.handler.close()
    
    def get_records(self, level: str = None) -> list:
        """Get captured log records, optionally filtered by level"""
        if level is None:
            return self.records
        
        level_num = getattr(logging, level.upper())
        return [record for record in self.records if record.levelno >= level_num]
    
    def get_messages(self, level: str = None) -> list:
        """Get captured log messages as strings"""
        records = self.get_records(level)
        return [record.getMessage() for record in records]


class PerformanceLogger:
    """Logger for performance metrics and timing"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.timers = {}
    
    def start_timer(self, name: str):
        """Start a named timer"""
        self.timers[name] = datetime.now()
        self.logger.debug(f"Started timer: {name}")
    
    def end_timer(self, name: str) -> float:
        """End a named timer and log the duration"""
        if name not in self.timers:
            self.logger.warning(f"Timer '{name}' was not started")
            return 0.0
        
        start_time = self.timers.pop(name)
        duration = (datetime.now() - start_time).total_seconds()
        
        self.logger.info(f"Timer '{name}': {duration:.3f} seconds")
        return duration
    
    def log_memory_usage(self, context: str = ""):
        """Log current memory usage"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            self.logger.info(f"Memory usage {context}: "
                           f"RSS={memory_info.rss / 1024 / 1024:.2f}MB, "
                           f"VMS={memory_info.vms / 1024 / 1024:.2f}MB")
        except ImportError:
            self.logger.debug("psutil not available for memory logging")
        except Exception as e:
            self.logger.error(f"Error logging memory usage: {e}")
    
    def log_system_info(self):
        """Log system information"""
        try:
            import psutil
            import platform
            
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.logger.info(f"System info: "
                           f"OS={platform.system()} {platform.release()}, "
                           f"CPU cores={cpu_count}, "
                           f"Memory={memory.total / 1024 / 1024 / 1024:.2f}GB, "
                           f"Disk={disk.total / 1024 / 1024 / 1024:.2f}GB")
        except ImportError:
            self.logger.debug("psutil not available for system info logging")
        except Exception as e:
            self.logger.error(f"Error logging system info: {e}")


def configure_third_party_logging():
    """Configure logging for third-party libraries"""
    # Reduce verbosity of common third-party libraries
    third_party_loggers = [
        'urllib3',
        'requests',
        'httpx',
        'asyncio',
        'concurrent.futures'
    ]
    
    for logger_name in third_party_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)


def get_logger(name: str) -> ContextualLogger:
    """Get a contextual logger instance"""
    logger = logging.getLogger(name)
    return ContextualLogger(logger)


# Initialize third-party logging configuration
configure_third_party_logging()
