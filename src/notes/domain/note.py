from pydantic import BaseModel
from datetime import datetime

from src.notes.domain.value_objects.content import NoteContent
from src.notes.domain.value_objects.id import Id
from src.notes.domain.value_objects.title import NoteTitle


class Note(BaseModel):
    id: Id
    title: NoteTitle
    content: NoteContent
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, title: str, content: str) -> "Note":
        """Factory method to create a new note"""
        return cls(
            id=Id.generate(),
            title=NoteTitle(value=title),
            content=NoteContent(value=content),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    def update_content(self, new_content: str) -> None:
        """Update the content of the note and the updated_at timestamp"""
        self.content = NoteContent(value=new_content)
        self.updated_at = datetime.utcnow()
