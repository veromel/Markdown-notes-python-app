from typing import Optional

from src.notes.domain.note import Note
from tests.mock.notes.domain.value_objects.content import NoteContentMother
from tests.mock.notes.domain.value_objects.title import TitleMother


class NoteMother:
    @staticmethod
    def create(
        title_value: Optional[str] = None, content_value: Optional[str] = None
    ) -> Note:
        title = TitleMother.create(title_value)
        content = NoteContentMother.create(content_value)
        return Note.create(title.value, content.value)
