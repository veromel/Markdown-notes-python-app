from typing import TypeVar, ClassVar
from datetime import datetime
from dataclasses import dataclass, field

from src.notes.domain.value_objects.content import NoteContent
from src.notes.domain.value_objects.id import Id
from src.notes.domain.value_objects.title import NoteTitle


@dataclass
class Note:
    id: Id
    title: NoteTitle
    content: NoteContent
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = None

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = self.created_at

    @staticmethod
    def create(title: str, content: str, user_id: str, note_id: str = None) -> "Note":
        return Note(
            id=Id(note_id),
            title=NoteTitle(value=title),
            content=NoteContent(value=content),
            user_id=user_id,
        )

    def update_title(self, new_title: str) -> None:
        self.title = NoteTitle(value=new_title)
        self.updated_at = datetime.utcnow()

    def update_content(self, new_content: str) -> None:
        self.content = NoteContent(value=new_content)
        self.updated_at = datetime.utcnow()
