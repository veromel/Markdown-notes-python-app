import re
from dataclasses import dataclass

from src.shared.domain.exceptions import ValidationException


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValidationException("El email no puede estar vacío")

        if not self._is_valid_email(self.value):
            raise ValidationException("El formato de email no es válido")

    def _is_valid_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        return self.value
