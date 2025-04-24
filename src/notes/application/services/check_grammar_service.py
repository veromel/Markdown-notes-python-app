import inject

from src.notes.application.dto.note_dto import (
    GrammarCheckInputDTO,
    GrammarCheckOutputDTO,
)
from src.notes.domain.repositories.note_repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.notes.infrastructure.language_tool.language_tool import get_language_tool
from src.shared.domain.exceptions import NotFoundException, AuthorizationException


class CheckGrammarService:
    @inject.autoparams()
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository
        self.language_tool = get_language_tool()

    async def check_note_grammar(
        self, input_dto: GrammarCheckInputDTO, user_id: str
    ) -> GrammarCheckOutputDTO:
        if input_dto.note_id:
            note = await self.note_repository.find_by_id(Id(input_dto.note_id))
            if not note:
                raise NotFoundException(
                    detail=f"Note with ID {input_dto.note_id} not found"
                )

            if note.user_id != user_id:
                raise AuthorizationException(
                    detail=f"User {user_id} is not authorized to check this note"
                )

        matches = self.language_tool.check(input_dto.content)
        errors = [match.message for match in matches]

        return GrammarCheckOutputDTO(errors=errors)

    async def check_text_grammar(
        self, input_dto: GrammarCheckInputDTO
    ) -> GrammarCheckOutputDTO:
        matches = self.language_tool.check(input_dto.content)
        errors = [match.message for match in matches]

        return GrammarCheckOutputDTO(errors=errors)
