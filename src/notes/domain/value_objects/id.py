from pydantic import BaseModel, Field, field_validator
import uuid


class Id(BaseModel):
    value: str = Field(...)

    @field_validator("value")
    def validate_id(cls, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format")
        return value

    @classmethod
    def generate(cls):
        return cls(value=str(uuid.uuid4()))
