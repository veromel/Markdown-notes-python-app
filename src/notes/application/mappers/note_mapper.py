from typing import List

from src.notes.domain.note import Note
from src.notes.application.dto.note_dto import (
    NoteInputDTO,
    NoteOutputDTO,
    NoteUpdateInputDTO,
)


class NoteMapper:
    @staticmethod
    def to_domain(dto: NoteInputDTO) -> Note:
        return Note.create(
            title=dto.title,
            content=dto.content,
            user_id=dto.user_id,
            note_id=dto.note_id,
        )

    @staticmethod
    def to_dto(note: Note) -> NoteOutputDTO:
        return NoteOutputDTO(
            id=str(note.id.value),
            title=note.title.value,
            content=note.content.value,
            user_id=note.user_id,
            created_at=note.created_at.isoformat(),
            updated_at=note.updated_at.isoformat() if note.updated_at else None,
        )

    @staticmethod
    def to_dto_list(notes: List[Note]) -> List[NoteOutputDTO]:
        return [NoteMapper.to_dto(note) for note in notes]
