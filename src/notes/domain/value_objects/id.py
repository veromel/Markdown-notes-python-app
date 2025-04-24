from pydantic import BaseModel, field_validator
import uuid
from typing import Any


class Id(BaseModel):
    value: str

    def __init__(self, value: str = None, **data: Any):
        if value is None:
            value = str(uuid.uuid4())
        if value == "undefined":
            raise ValueError("El ID no puede ser 'undefined'")
        if not value.strip():
            raise ValueError("El ID no puede estar vacío")
        super().__init__(value=value, **data)

    @field_validator("value")
    def validate_id(cls, value):
        if value == "undefined":
            raise ValueError("El ID no puede ser 'undefined'")
        if not value.strip():
            raise ValueError("El ID no puede estar vacío")
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(f"Formato de UUID inválido: {value}")
        return value

    @classmethod
    def generate(cls):
        return cls(str(uuid.uuid4()))
