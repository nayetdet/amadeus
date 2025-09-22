import logging
from typing import Optional

class LoggerInstance:
    __error_logger: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls.__error_logger is None:
            cls.__error_logger = logging.getLogger("uvicorn.error")
        return cls.__error_logger
