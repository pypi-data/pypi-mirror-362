# Stdlib imports
from pathlib import Path
import logging
import logging.handlers


# Third-party app imports

# Imports from your apps
from code_runner_files.Config import LogConfig


class LogClass(object):
    log_file_path = str(Path(LogConfig.LOG_DIR, LogConfig.LOGS_FILE_NAME))
    logging_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    log_format = "[%(levelname)s] %(asctime)s RAI PSM [%(name)s (%(lineno)d)]: %(message)s"
    formatter = logging.Formatter(fmt=log_format, datefmt="%d/%m/%Y %I:%M:%S %p")
    log_handlers = list()

    if LogConfig.FILE_HANDLER:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path, maxBytes=LogConfig.LOG_MAX_FILE_SIZE, backupCount=5
        )
        file_handler.setFormatter(formatter)
        log_handlers.append(file_handler)

    if LogConfig.CONSOLE_HANDLER:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        log_handlers.append(console_handler)

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        for handler in LogClass.log_handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(LogClass.logging_levels.get(LogConfig.LEVEL.upper(), logging.WARN))

    def log_debug(self, log_message):
        self.logger.debug(log_message)

    def log_info(self, log_message):
        self.logger.info(log_message)

    def log_warning(self, log_message):
        self.logger.warning(log_message)

    def log_exception(self, log_message):
        self.logger.exception(log_message)

    def log_error(self, log_message):
        self.logger.error(log_message)

    def log_critical(self, log_message):
        self.logger.critical(log_message)
