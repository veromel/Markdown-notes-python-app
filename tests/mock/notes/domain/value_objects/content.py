from typing import Optional
from src.notes.domain.value_objects.content import NoteContent
from tests.mock.mother_creator import MotherCreator


class NoteContentMother:
    @staticmethod
    def create(value: Optional[str] = None) -> NoteContent:
        return NoteContent(
            value=value or MotherCreator.random().paragraph(nb_sentences=3)
        )
