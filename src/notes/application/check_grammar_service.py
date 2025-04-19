import inject
from typing import List, Optional

from src.notes.domain.repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.notes.infrastructure.language_tool.language_tool import get_language_tool
from src.shared.domain.exceptions import (
    NotFoundException,
    AuthorizationException,
    ValidationException,
)


class CheckGrammarService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository
        self.language_tool = get_language_tool()

    async def check_note_grammar(
        self, note_id: str, content: str, user_id: str
    ) -> List[str]:
        # Validar que el contenido no esté vacío
        if not content:
            raise ValidationException("Content cannot be empty")

        # Verificar existencia y autorización
        note = await self.note_repository.find_by_id(Id(note_id))
        if not note:
            raise NotFoundException("Note not found")

        # Verificar autorización - ahora siempre es obligatorio
        if note.user_id != user_id:
            raise AuthorizationException("You are not allowed to check this note")

        # Verificar gramática
        matches = self.language_tool.check(content)
        return [match.message for match in matches]

    async def check_text_grammar(self, content: str) -> List[str]:
        # Validar que el contenido no esté vacío
        if not content:
            raise ValidationException("Content cannot be empty")

        # Verificar gramática
        matches = self.language_tool.check(content)
        return [match.message for match in matches]
