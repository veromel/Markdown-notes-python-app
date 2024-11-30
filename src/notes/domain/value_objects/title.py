from pydantic import BaseModel, Field, field_validator


class NoteTitle(BaseModel):
    value: str = Field(..., max_length=255)

    @field_validator("value")
    def validate_title(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title cannot be empty")
        if len(value) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        return value
