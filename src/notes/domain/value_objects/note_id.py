from pydantic import BaseModel, validator
import uuid


class NoteID(BaseModel):
    value: str

    @validator("value")
    def validate_id(cls, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format")
        return value

    @classmethod
    def generate(cls):
        return cls(value=str(uuid.uuid4()))
