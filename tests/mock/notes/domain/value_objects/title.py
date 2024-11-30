from typing import Optional
from src.notes.domain.value_objects.title import NoteTitle
from tests.mock.mother_creator import MotherCreator


class TitleMother:
    @staticmethod
    def create(value: Optional[str] = None) -> NoteTitle:
        return NoteTitle(value=value or MotherCreator.random().sentence(nb_words=6))
