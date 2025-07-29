import enum
import logging
import os

from kink import di


class LogLevel(str, enum.Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'


class DuplicateFilter(logging.Filter):

    def filter(self, record):
        # add other fields if you need more granular comparison, depends on your app
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False


class LoggerFactory:

    def __init__(self):
        self._app_name = os.getenv("APP_NAME")
        if not self._app_name:
            raise ValueError("Env value with key 'APP_NAME' not set.")
        self._log_level = os.getenv("LOG_LEVEL")
        if not self._log_level:
            raise ValueError("Env value with key 'LOG_LEVEL' not set.")
        self._logger_file_name = os.getenv("LOGGER_FILE")
        if not self._logger_file_name:
            raise ValueError("Env value with key 'LOGGER_FILE' not set.")
        self._logger_file_path = os.getenv("LOGGER_FILE_PATH")
        if not self._logger_file_path:
            raise ValueError("Env value with key 'LOGGER_FILE_PATH' not set.")

        self._logger_file = self._set_logger_file()
        self._logger = self._init_logger()

    def _init_logger(self):
        logging.basicConfig(
            encoding='utf-8'  # Ensure UTF-8 encoding
        )
        logger = logging.getLogger(self._app_name)
        logger.addFilter(DuplicateFilter())
        logger.propagate = False

        if self._log_level == LogLevel.DEBUG:
            logger.setLevel(logging.DEBUG)
        elif self._log_level == LogLevel.INFO:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")

        file_logging = logging.FileHandler(self._logger_file)
        file_logging.setFormatter(formatter)
        logger.addHandler(file_logging)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def get_logger(self):
        return self._logger

    def _set_logger_file(self):
        # user_home_dir = os.path.expanduser("~")
        logger_file = os.path.join(self._logger_file_path, self._logger_file_name)
        if not os.path.exists(logger_file):
            try:
                os.makedirs(logger_file.removesuffix(self._logger_file_name))
            except FileExistsError as fx:
                print("Log file already exists")
        return logger_file


di['logger'] = lambda _di: LoggerFactory().get_logger()
