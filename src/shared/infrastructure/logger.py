"""StdoutLogger."""

import json
import logging

from src.shared.domain.logger import Logger

FORMAT = '{"level": "%(levelname)s", "occurred_on": "%(asctime)s", %(message)s}'


class StdoutLogger(Logger):
    def __init__(self):
        self.logger = logging.Logger("querix")
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)

    def __make(
        self,
        message: str,
        code: str | None = None,
        details: dict | None = None,
    ) -> str:
        log = {"message": message}
        if code:
            log["code"] = code
        if details:
            log["details"] = details
        return json.dumps(log, ensure_ascii=False)[1:-1]

    def debug(
        self,
        message: str,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        log = self.__make(message, code, details)
        self.logger.debug(log)

    def info(
        self,
        message: str,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        log = self.__make(message, code, details)
        self.logger.info(log)

    def warning(
        self,
        message: str,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        log = self.__make(message, code, details)
        self.logger.warning(log)

    def error(
        self,
        message: str,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        log = self.__make(message, code, details)
        self.logger.error(log)

    def critical(
        self,
        message: str,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        log = self.__make(message, code, details)
        self.logger.critical(log)
