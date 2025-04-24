import pytest
import uuid
from unittest.mock import AsyncMock
from pydantic import ValidationError
from src.notes.application.services.update_note_service import UpdateNoteService
from src.notes.domain.repositories.note_repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.notes.application.dto.note_dto import NoteUpdateInputDTO
from src.shared.domain.exceptions import (
    ValidationException,
    NotFoundException,
    AuthorizationException,
)


@pytest.mark.unit
class TestUpdateNoteService:

    def setup_method(self):
        self.repository = AsyncMock(NoteRepository)
        self.service = UpdateNoteService(self.repository)

    @pytest.mark.asyncio
    async def test_update_note_successful(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id
        new_title = "Nuevo título"
        new_content = "Nuevo contenido"

        self.repository.find_by_id.return_value = sample_note

        input_dto = NoteUpdateInputDTO(
            id=note_id, title=new_title, content=new_content, user_id=user_id
        )
        await self.service(input_dto)

        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.repository.update.assert_called_once()

        updated_note = self.repository.update.call_args.args[0]
        assert updated_note.title.value == new_title
        assert updated_note.content.value == new_content
        assert updated_note.updated_at is not None

    @pytest.mark.asyncio
    async def test_update_note_not_found(self):
        note_id = str(uuid.uuid4())  # UUID válido
        new_title = "Nuevo título"
        new_content = "Nuevo contenido"
        user_id = "test-user-id"

        self.repository.find_by_id.return_value = None

        with pytest.raises(NotFoundException) as excinfo:
            input_dto = NoteUpdateInputDTO(
                id=note_id, title=new_title, content=new_content, user_id=user_id
            )
            await self.service(input_dto)

        assert isinstance(excinfo.value, NotFoundException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_note_repository_error(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id
        new_title = "Nuevo título"
        new_content = "Nuevo contenido"

        self.repository.find_by_id.return_value = sample_note
        self.repository.update.side_effect = Exception("Error updating note")

        with pytest.raises(Exception) as excinfo:
            input_dto = NoteUpdateInputDTO(
                id=note_id, title=new_title, content=new_content, user_id=user_id
            )
            await self.service(input_dto)

        assert "Error updating note" in str(excinfo.value)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_note_unauthorized(self, note):
        sample_note = note(user_id="user-1")
        note_id = str(sample_note.id.value)
        invalid_user_id = "user-2"  # Diferente al user_id de la nota
        new_title = "Nuevo título"
        new_content = "Nuevo contenido"

        self.repository.find_by_id.return_value = sample_note

        with pytest.raises(AuthorizationException) as excinfo:
            input_dto = NoteUpdateInputDTO(
                id=note_id,
                title=new_title,
                content=new_content,
                user_id=invalid_user_id,
            )
            await self.service(input_dto)

        assert isinstance(excinfo.value, AuthorizationException)
        self.repository.find_by_id.assert_called_once_with(Id(note_id))
        self.repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_note_empty_title(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id
        empty_title = ""
        new_content = "Nuevo contenido"

        self.repository.find_by_id.return_value = sample_note

        with pytest.raises(ValidationError):
            input_dto = NoteUpdateInputDTO(
                id=note_id, title=empty_title, content=new_content, user_id=user_id
            )

        self.repository.find_by_id.assert_not_called()
        self.repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_note_empty_content(self, note):
        sample_note = note()
        note_id = str(sample_note.id.value)
        user_id = sample_note.user_id
        new_title = "Nuevo título"
        empty_content = ""

        self.repository.find_by_id.return_value = sample_note

        with pytest.raises(ValidationError):
            input_dto = NoteUpdateInputDTO(
                id=note_id, title=new_title, content=empty_content, user_id=user_id
            )

        self.repository.find_by_id.assert_not_called()
        self.repository.update.assert_not_called()
