from abc import ABC, abstractmethod
from typing import List, Optional
from src.notes.domain.note import Note


class NoteRepository(ABC):
    @abstractmethod
    async def save(self, note: Note) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, note_id: str) -> Optional[Note]:
        pass

    @abstractmethod
    async def find_all(self) -> List[Note]:
        pass

    @abstractmethod
    async def update(self, note: Note) -> None:
        pass

    @abstractmethod
    async def delete(self, note_id: str) -> None:
        pass
