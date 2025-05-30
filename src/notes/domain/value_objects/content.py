from pydantic import BaseModel, Field, field_validator


class NoteContent(BaseModel):
    value: str = Field(...)

    @field_validator("value")
    def validate_content(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError("Content cannot be empty")
        return value
