from pydantic import BaseModel, validator

class NoteContent(BaseModel):
    value: str

    @validator("value")
    def validate_content(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError("Content cannot be empty")
        return value