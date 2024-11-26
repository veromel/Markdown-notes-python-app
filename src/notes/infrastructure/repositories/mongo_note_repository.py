from src.notes.domain.note import Note
from src.notes.infrastructure.db.mongodb import get_mongo_client
from typing import List, Optional
from uuid import UUID
from pydantic import parse_obj_as


class MongoNoteRepository:
    def __init__(self):
        self.collection = None

    async def initialize(self):
        if self.collection is None:
            db = await get_mongo_client()
            self.collection = db['notes']

    async def save(self, note: Note) -> None:
        await self.initialize()
        await self.collection.insert_one(note.dict())

    async def find_by_id(self, note_id: UUID) -> Optional[Note]:
        await self.initialize()
        note_data = await self.collection.find_one({"id": str(note_id)})
        return Note.parse_obj(note_data) if note_data else None

    async def find_all(self) -> List[Note]:
        await self.initialize()
        notes_cursor = self.collection.find()
        notes_data = await notes_cursor.to_list(length=None)
        return parse_obj_as(List[Note], notes_data)

    async def update(self, note: Note) -> bool:
        await self.initialize()
        result = await self.collection.update_one(
            {"id": str(note.id)},
            {"$set": note.dict()}
        )
        return result.modified_count > 0

    async def delete(self, note_id: UUID) -> bool:
        await self.initialize()
        result = await self.collection.delete_one({"id": str(note_id)})
        return result.deleted_count > 0


