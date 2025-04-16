from typing import TypeVar, ClassVar

from pydantic import BaseModel
from datetime import datetime

from src.notes.domain.value_objects.content import NoteContent
from src.notes.domain.value_objects.id import Id
from src.notes.domain.value_objects.title import NoteTitle

# Crear un TypeVar para Note
T = TypeVar("T", bound="Note")


class Note(BaseModel):
    id: Id
    title: NoteTitle
    content: NoteContent
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def create(
        cls,
        id: str,
        title: str,
        content: str,
    ) -> T:
        return cls(
            id=Id(id),
            title=NoteTitle(value=title),
            content=NoteContent(value=content),
            created_at=datetime.utcnow(),
            updated_at=None,
        )

    def update_title(self, new_title: str) -> None:
        self.title = NoteTitle(value=new_title)
        self.updated_at = datetime.utcnow()

    def update_content(self, new_content: str) -> None:
        self.content = NoteContent(value=new_content)
        self.updated_at = datetime.utcnow()
