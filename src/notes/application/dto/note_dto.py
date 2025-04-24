from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class NoteInputDTO(BaseModel):
    title: str = Field(..., min_length=1, description="Note title")
    content: str = Field(..., min_length=1, description="Note content")
    user_id: Optional[str] = Field("", description="User id")
    note_id: Optional[str] = Field(None, description="Note id")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Mi nota importante",
                "content": "Contenido de la nota con formato markdown",
            }
        }
    }


class NoteOutputDTO(BaseModel):
    id: str
    title: str
    content: str
    user_id: str
    created_at: str
    updated_at: Optional[str] = None


class NoteUpdateInputDTO(BaseModel):
    id: str = Field(..., description="Note to update id")
    title: str = Field(..., min_length=1, description="New title")
    content: str = Field(..., min_length=1, description="New content")
    user_id: Optional[str] = Field("", description="User id")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "title": "Título actualizado",
                "content": "Contenido actualizado de la nota",
            }
        }
    }


class NoteListOutputDTO(BaseModel):
    notes: List[NoteOutputDTO]


class GrammarCheckInputDTO(BaseModel):
    content: str = Field(..., min_length=1, description="Text to review")
    note_id: Optional[str] = Field(None, description="Note id")

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v


class GrammarCheckOutputDTO(BaseModel):
    errors: List[str] = Field(...)
