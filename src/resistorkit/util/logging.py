import time
import os
import atexit
from datetime import datetime
from enum import Enum


# Color codes for terminal output
class Colors:
    HEADER = "\033[95m"
    INFO = "\033[94m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    ENDC = "\033[0m"
    DEBUG = "\033[96m"


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class Logger:
    """
    A simple logger class for logging messages to the console and a log file.

    Example:
        log_manager = LogManager()
        logger = Logger(log_manager)
        logger.info("This is an info message")

    Features:
    - Log messages are color-coded for better readability.
    - Log messages are written to a log file.
    - Log messages are timestamped.
    - Log messages are prefixed with the log level.
    - Log messages include the elapsed time since the script started.
    """

    def __init__(self, app_name="App", log_dir='logs', max_logs=5, log_level=LogLevel.INFO, log_timefmt="%Y-%m-%d %H:%M:%S", log_filename_prefix="log-"):
        # Initialize log manager
        self.app_name = app_name
        self.log_dir = log_dir
        self.max_logs = max_logs
        self.log_level = log_level
        self.log_timefmt = log_timefmt
        self.log_filename_prefix = log_filename_prefix

        self.start_time = time.time()

        # Ensure logs directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Rotate old logs
        self._rotate_logs()

        # Setup new log file
        self.log_file = (
            f"{log_dir}/{self.log_filename_prefix}{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        self.log_handler = open(self.log_file, "a")

        # Register cleanup
        atexit.register(self.cleanup)

    def _rotate_logs(self):
        """Remove old log files if we exceed max_logs"""
        logs = sorted(
            [
                f
                for f in os.listdir(self.log_dir)
                if f.startswith(self.log_filename_prefix)
            ]
        )
        while len(logs) >= self.max_logs:
            os.remove(os.path.join(self.log_dir, logs[0]))
            logs.pop(0)

    def _format_message(self, level, msg):
        """Format log message with timestamp, elapsed time, and log level"""
        timestamp = datetime.now().strftime(self.log_timefmt)
        elapsed = f"{time.time() - self.start_time:.2f}s"
        return f"[{timestamp}] [{self.app_name} {elapsed}] [{level.name}] {msg}"

    def _write(self, level, msg, color=""):
        if level.value >= self.log_level.value:
            formatted_msg = self._format_message(level, msg)
            print(f"{color}{formatted_msg}{Colors.ENDC}")
            self.log_handler.write(f"{formatted_msg}\n")
            self.log_handler.flush()

    def cleanup(self):
        """Close log file handler"""
        if hasattr(self, "log_handler"):
            self.log_handler.close()

    def set_log_level(self, level: LogLevel):
        """Set the log level"""
        self.log_level = level

    def debug(self, msg):
        """Log a debug message"""
        self._write(LogLevel.DEBUG, msg, Colors.DEBUG)

    def info(self, msg):
        """Log an info message"""
        self._write(LogLevel.INFO, msg, Colors.INFO)

    def warning(self, msg):
        """Log a warning message"""
        self._write(LogLevel.WARNING, msg, Colors.WARNING)

    def error(self, msg):
        """Log an error message"""
        self._write(LogLevel.ERROR, msg, Colors.ERROR)

    def custom(self, msg, color):
        """Log a custom message with a specific color"""
        self._write(LogLevel.INFO, msg, color)
