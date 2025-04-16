from motor.motor_asyncio import AsyncIOMotorClient
from bson import Binary

from src.notes.domain.note import Note
from src.notes.domain.repository import NoteRepository
from typing import List, Optional
from uuid import UUID

from src.notes.infrastructure.repositories.schema import NoteSchema


class MongoNoteRepository(NoteRepository):
    def __init__(self, client: AsyncIOMotorClient, mongodb_name: str):
        self.database = client[mongodb_name]
        self.collection = self.database["notes"]

    async def save(self, note: Note) -> None:
        doc = NoteSchema.to_mongo(note)
        await self.collection.insert_one(doc)

    async def find_by_id(self, note_id: str) -> Optional[Note]:
        uuid_obj = UUID(note_id)
        binary_uuid = Binary.from_uuid(uuid_obj)

        note_data = await self.collection.find_one({"_id": binary_uuid})
        return NoteSchema.to_domain(note_data)

    async def find_all(self) -> List[Note]:
        notes_cursor = self.collection.find()
        notes_data = await notes_cursor.to_list(length=None)
        return [
            NoteSchema.to_domain(note_data) for note_data in notes_data if note_data
        ]

    async def update(self, note: Note) -> None:
        doc = NoteSchema.to_mongo(note)
        binary_id = doc.pop("_id")

        update_data = {
            "title": note.title.value,
            "content": note.content.value,
            "updated_at": note.updated_at,
        }

        await self.collection.update_one({"_id": binary_id}, {"$set": update_data})

    async def delete(self, note_id: str) -> None:
        uuid_obj = UUID(note_id)
        binary_uuid = Binary.from_uuid(uuid_obj)

        await self.collection.delete_one({"_id": binary_uuid})
