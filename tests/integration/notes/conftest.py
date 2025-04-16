import pytest
import uuid

from src.notes.domain.note import Note
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)
from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id


@pytest.fixture
def note_repository(mongo_client, default_mongo_database) -> NoteRepository:
    """Repositorio MongoNoteRepository para los tests"""
    print(f"🔧 Creando repositorio: {default_mongo_database}")
    repo = MongoNoteRepository(client=mongo_client, mongodb_name=default_mongo_database)
    return repo


@pytest.fixture
def note(faker):
    def _create(**kwargs):
        note_id = kwargs.get("id") or Id.generate().value
        title_value = kwargs.get("title") or faker.sentence()
        content_value = kwargs.get("content") or faker.paragraph()

        note = Note.create(id=note_id, title=title_value, content=content_value)
        return note

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


@pytest.fixture
def persisted_note(note_repository, note):
    async def _create(**kwargs):
        sample_note = note(**kwargs)
        note_id = sample_note.id.value
        try:
            await note_repository.save(sample_note)
        except Exception as e:
            print(f"Error al persistir nota {note_id}: {e}")
        return sample_note

    return _create


@pytest.fixture
def persisted_notes(note_repository, notes):
    async def _create(count=3, **kwargs):
        sample_notes = notes(count=count, **kwargs)
        for note in sample_notes:
            note_id = note.id.value
            try:
                await note_repository.save(note)
            except Exception as e:
                print(f"Error al persistir nota {note_id}: {e}")
        return sample_notes

    return _create
