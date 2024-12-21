import logging
from logging.handlers import RotatingFileHandler
from threading import Lock


class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialize_logger()
            return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger("ThreadSafeLogger")
        self.logger.setLevel(logging.DEBUG)

        # Rotating File Handler (Thread-Safe)
        file_handler = RotatingFileHandler('app.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Adding Handler
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

    # Convenience methods for logging
    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def sanitize_body(self, body):
        """
        Redacts sensitive information like passwords from the request body.
        """
        if not isinstance(body, dict):
            return body

        redacted_body = body.copy()
        sensitive_keys = {"password", "token", "secret"}  # Add other sensitive keys as needed
        for key in sensitive_keys:
            if key in redacted_body:
                redacted_body[key] = "***"  # Mask the sensitive value
        return redacted_body
