"""
Fixtures para tests unitarios de notas
"""

import pytest

from src.notes.domain.note import Note
from src.notes.domain.value_objects.id import Id
from src.notes.domain.value_objects.title import NoteTitle
from src.notes.domain.value_objects.content import NoteContent


@pytest.fixture
def note(faker):
    def _create(**kwargs):
        note_id = kwargs.get("id") or Id.generate().value
        title_value = kwargs.get("title") or faker.sentence()
        content_value = kwargs.get("content") or faker.paragraph()
        user_id = kwargs.get("user_id") or "test-user-id"

        return Note.create(
            title=title_value, content=content_value, user_id=user_id, note_id=note_id
        )

    return _create


@pytest.fixture
def notes(faker):
    def _create_notes(count: int = 3, **kwargs) -> list[Note]:
        result = []
        for i in range(count):
            note_id = kwargs.get("id") or Id.generate().value
            title_value = kwargs.get("title") or faker.sentence()
            content_value = kwargs.get("content") or faker.paragraph()
            user_id = kwargs.get("user_id") or "test-user-id"

            note = Note.create(
                title=title_value,
                content=content_value,
                user_id=user_id,
                note_id=note_id,
            )
            result.append(note)

        return result

    return _create_notes
