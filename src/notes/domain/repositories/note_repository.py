from abc import ABC, abstractmethod
from typing import List, Optional

from src.notes.domain.note import Note
from src.notes.domain.value_objects.id import Id


class NoteRepository(ABC):
    @abstractmethod
    async def save(self, note: Note) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, id: Id) -> Optional[Note]:
        pass

    @abstractmethod
    async def find_all(self) -> List[Note]:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Note]:
        pass

    @abstractmethod
    async def delete(self, id: Id) -> None:
        pass
