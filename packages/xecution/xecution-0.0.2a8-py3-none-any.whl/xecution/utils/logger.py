import logging
import colorlog
from logging.handlers import TimedRotatingFileHandler
from typing import List

class Logger:
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    def __init__(
        self,
        log_level: int = logging.INFO,
        log_file: str = "strategy.log",
        handlers: List[logging.Handler] = [],
    ):
        """
        Initializes the logger with color output and file rotation.
        """
        self.handlers = handlers

        if not self.handlers:
            # Colored console handler
            color_handler = colorlog.StreamHandler()
            color_handler.setFormatter(
                colorlog.ColoredFormatter(
                    f"%(log_color)s{self.LOG_FORMAT}",
                    log_colors={
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red',
                    }
                )
            )

            # Timed rotating file handler (rotates every hour, keeps 30 backups)
            file_handler = TimedRotatingFileHandler(
                log_file, when="h", interval=1, backupCount=30, encoding='utf-8'
            )
            file_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
            file_handler.setLevel(log_level)

            self.handlers = [color_handler, file_handler]

        # Apply handlers to root logger
        logging.root.setLevel(log_level)
        for handler in self.handlers:
            if handler not in logging.root.handlers:
                logging.root.addHandler(handler)
