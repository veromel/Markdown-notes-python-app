from motor.motor_asyncio import AsyncIOMotorClient
from bson import Binary
from typing import List, Optional
from uuid import UUID
from pymongo.collection import Collection

from src.notes.domain.note import Note
from src.notes.domain.repositories.note_repository import NoteRepository
from src.notes.domain.value_objects.id import Id
from src.notes.infrastructure.repositories.schema import NoteSchema


class MongoNoteRepository(NoteRepository):
    def __init__(self, client: AsyncIOMotorClient, mongodb_name: str):
        self.database = client[mongodb_name]
        self.collection = self.database["notes"]

    async def save(self, note: Note) -> None:
        doc = NoteSchema.to_mongo(note)
        await self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)

    async def find_by_id(self, id: Id) -> Optional[Note]:
        uuid_obj = UUID(str(id.value))
        binary_uuid = Binary.from_uuid(uuid_obj)

        note_data = await self.collection.find_one({"_id": binary_uuid})
        return NoteSchema.to_domain(note_data) if note_data else None

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

    async def delete(self, note_id: Id) -> None:
        if isinstance(note_id, Id):
            note_id_str = note_id.value
        else:
            note_id_str = str(note_id)

        uuid_obj = UUID(note_id_str)
        binary_uuid = Binary.from_uuid(uuid_obj)

        await self.collection.delete_one({"_id": binary_uuid})

    async def find_by_user_id(self, user_id: str) -> List[Note]:
        notes_cursor = self.collection.find({"user_id": user_id})
        notes_data = await notes_cursor.to_list(length=None)
        return [
            NoteSchema.to_domain(note_data) for note_data in notes_data if note_data
        ]
