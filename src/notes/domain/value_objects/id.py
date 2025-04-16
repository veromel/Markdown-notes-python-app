from pydantic import BaseModel, field_validator
import uuid
from typing import Any


class Id(BaseModel):
    value: str

    def __init__(self, value: str = None, **data: Any):
        if value is None:
            value = str(uuid.uuid4())
        super().__init__(value=value, **data)

    @field_validator("value")
    def validate_id(cls, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format")
        return value

    @classmethod
    def generate(cls):
        return cls(str(uuid.uuid4()))
