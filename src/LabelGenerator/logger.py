import logging
import os
import sys
from datetime import datetime

class LabelLogger:
    """
    Logger management class for the LabelGenerator library
    Used to record various information about library operations, supports console and file output
    """
    
    # Log level mapping
    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    _instance = None
    
    @classmethod
    def get_logger(cls, name='LabelGenerator'):
        """
        Get logger instance (singleton pattern)
        
        Args:
            name: Logger name, default is 'LabelGenerator'
            
        Returns:
            LabelLogger instance
        """
        if cls._instance is None:
            cls._instance = cls(name)
        return cls._instance
    
    def __init__(self, name='LabelGenerator'):
        """
        Initialize logger
        
        Args:
            name: Logger name, default is 'LabelGenerator'
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)  # Default log level
        self.log_file = None
        self.console_handler = None
        self.file_handler = None
        
        # Set up default handler (console output)
        self._setup_console_handler()
    
    def _setup_console_handler(self):
        """Set up console log handler"""
        if self.console_handler is not None:
            self.logger.removeHandler(self.console_handler)
            
        self.console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
        self.console_handler.setFormatter(formatter)
        self.logger.addHandler(self.console_handler)
    
    def set_level(self, level):
        """
        Set log level
        
        Args:
            level: Log level, can be a string ('debug', 'info', 'warning', 'error', 'critical')
                  or logging module level constants
        """
        if isinstance(level, str):
            level = level.lower()
            if level in self.LOG_LEVELS:
                self.logger.setLevel(self.LOG_LEVELS[level])
                self.debug(f"Log level set to: {level}")
            else:
                self.warning(f"Unknown log level: {level}, using default level (INFO)")
        else:
            self.logger.setLevel(level)
            self.debug(f"Log level set to: {level}")
    
    def enable_file_logging(self, log_dir=None, log_file=None):
        """
        Enable file logging
        
        Args:
            log_dir: Log directory, default is 'logs' subdirectory in the current working directory
            log_file: Log filename, default is 'labelgenerator_YYYYMMDD_HHMMSS.log'
        """
        if log_dir is None:
            # Default to 'logs' subdirectory in the current working directory
            log_dir = os.path.join(os.getcwd(), 'logs')
            
        # Ensure log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        if log_file is None:
            # Default to timestamped filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f'labelgenerator_{timestamp}.log'
            
        self.log_file = os.path.join(log_dir, log_file)
        
        # Remove existing file handler if present
        if self.file_handler is not None:
            self.logger.removeHandler(self.file_handler)
            
        # Create new file handler
        self.file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
        self.file_handler.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)
        
        self.info(f"File logging enabled: {self.log_file}")
    
    def disable_file_logging(self):
        """Disable file logging"""
        if self.file_handler is not None:
            self.logger.removeHandler(self.file_handler)
            self.file_handler = None
            self.info("File logging disabled")
    
    def log_registered_fonts(self):
        """Log list of currently registered fonts, for debugging"""
        try:
            from reportlab.pdfbase import pdfmetrics
            registered_fonts = pdfmetrics.getRegisteredFontNames()
            self.info(f"Number of registered fonts: {len(registered_fonts)}")
            for font in sorted(registered_fonts):
                self.debug(f"Registered font: {font}")
        except ImportError:
            self.warning("Cannot import reportlab module, unable to display registered fonts list")
        except Exception as e:
            self.error(f"Error getting registered fonts list: {e}")
    
    # Proxy log methods
    def debug(self, message):
        """Log DEBUG level message"""
        self.logger.debug(message)
        
    def info(self, message):
        """Log INFO level message"""
        self.logger.info(message)
        
    def warning(self, message):
        """Log WARNING level message"""
        self.logger.warning(message)
        
    def error(self, message):
        """Log ERROR level message"""
        self.logger.error(message)
        
    def critical(self, message):
        """Log CRITICAL level message"""
        self.logger.critical(message)
        
    def exception(self, message):
        """Log exception information, including stack trace"""
        self.logger.exception(message)

# Create a default logger instance for easy import and use
logger = LabelLogger.get_logger()
