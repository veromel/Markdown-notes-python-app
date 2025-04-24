import pytest

from src.notes.domain.note import Note
from src.notes.domain.value_objects.id import Id


@pytest.mark.integration
@pytest.mark.asyncio(scope="session")
class TestNoteRepository:

    async def test_save_and_find_by_id(self, note_repository, note):
        sample_note = note()
        note_id = sample_note.id.value

        await note_repository.save(sample_note)
        retrieved_note = await note_repository.find_by_id(Id(note_id))

        assert retrieved_note is not None
        assert str(retrieved_note.id.value) == note_id
        assert retrieved_note.title.value == sample_note.title.value
        assert retrieved_note.content.value == sample_note.content.value

    async def test_find_all(self, note_repository, persisted_notes):
        expected_notes = await persisted_notes(count=3)

        all_notes = await note_repository.find_all()

        assert len(all_notes) >= 3
        assert all(isinstance(note, Note) for note in all_notes)

        created_ids = [note.id.value for note in expected_notes]
        retrieved_ids = [note.id.value for note in all_notes]
        for created_id in created_ids:
            assert created_id in retrieved_ids

    async def test_find_by_user_id(self, note_repository, persisted_notes, faker):
        user_id = f"test-user-{faker.uuid4()}"
        expected_notes = await persisted_notes(count=3, user_id=user_id)
        other_user_id = f"other-user-{faker.uuid4()}"
        await persisted_notes(count=2, user_id=other_user_id)

        user_notes = await note_repository.find_by_user_id(user_id)

        assert len(user_notes) == 3
        assert all(isinstance(note, Note) for note in user_notes)
        assert all(note.user_id == user_id for note in user_notes)

        created_ids = [note.id.value for note in expected_notes]
        retrieved_ids = [note.id.value for note in user_notes]
        for created_id in created_ids:
            assert created_id in retrieved_ids

    async def test_delete_note(self, note_repository, persisted_note):
        sample_note = await persisted_note()
        note_id = sample_note.id.value

        await note_repository.delete(Id(note_id))

        deleted_note = await note_repository.find_by_id(Id(note_id))
        assert deleted_note is None

    async def test_update(self, note_repository, persisted_note, faker):
        sample_note = await persisted_note()
        note_id = sample_note.id.value

        new_title = faker.sentence()
        new_content = faker.paragraph()

        sample_note.update_title(new_title)
        sample_note.update_content(new_content)

        await note_repository.update(sample_note)

        updated_note = await note_repository.find_by_id(Id(note_id))
        assert updated_note is not None
        assert updated_note.title.value == new_title
        assert updated_note.content.value == new_content
