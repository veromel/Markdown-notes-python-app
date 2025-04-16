"""
Fixtures para tests unitarios de notas
"""

import pytest
from datetime import datetime
from typing import Optional, Callable, Any

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
        created_at = kwargs.get("created_at") or datetime.utcnow()
        updated_at = kwargs.get("updated_at") or None

        return Note.create(id=note_id, title=title_value, content=content_value)

    return _create


@pytest.fixture
def notes(faker):
    def _create_notes(count: int = 3, **kwargs) -> list[Note]:
        result = []
        for i in range(count):
            note_id = kwargs.get("id") or Id.generate().value
            title_value = kwargs.get("title") or faker.sentence()
            content_value = kwargs.get("content") or faker.paragraph()
            note = Note.create(id=note_id, title=title_value, content=content_value)
            result.append(note)

        return result

    return _create_notes
