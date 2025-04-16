from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def debug(
        self, message: str, code: str | None = None, details: dict | None = None
    ) -> None: ...

    @abstractmethod
    def info(
        self, message: str, code: str | None = None, details: dict | None = None
    ) -> None: ...

    @abstractmethod
    def warning(
        self, message: str, code: str | None = None, details: dict | None = None
    ) -> None: ...

    @abstractmethod
    def error(
        self, message: str, code: str | None = None, details: dict | None = None
    ) -> None: ...
