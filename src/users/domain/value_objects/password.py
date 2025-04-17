import re
from dataclasses import dataclass
import bcrypt

from src.shared.domain.exceptions import ValidationException


@dataclass(frozen=True)
class Password:
    value: str
    is_hashed: bool = False

    def __post_init__(self):
        if not self.value:
            raise ValidationException("La contraseña no puede estar vacía")

        if not self.is_hashed and not self._is_valid_password(self.value):
            raise ValidationException(
                "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número"
            )

    def _is_valid_password(self, password: str) -> bool:
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        return bool(re.match(pattern, password))

    def hash(self) -> "Password":
        if self.is_hashed:
            return self

        hashed = bcrypt.hashpw(self.value.encode(), bcrypt.gensalt()).decode()
        return Password(value=hashed, is_hashed=True)

    def check(self, plain_password: str) -> bool:
        if not self.is_hashed:
            return False

        return bcrypt.checkpw(plain_password.encode(), self.value.encode())

    def __str__(self) -> str:
        return "[PROTECTED]"
