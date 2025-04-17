import datetime
from uuid import UUID
from bson import Binary

from src.notes.domain.note import Note
from src.notes.domain.value_objects.id import Id
from src.notes.domain.value_objects.title import NoteTitle
from src.notes.domain.value_objects.content import NoteContent


class NoteSchema:
    @staticmethod
    def to_mongo(note: Note) -> dict:
        uuid_obj = UUID(str(note.id.value))
        binary_uuid = Binary.from_uuid(uuid_obj)

        return {
            "_id": binary_uuid,
            "title": note.title.value,
            "content": note.content.value,
            "user_id": note.user_id,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }

    @staticmethod
    def to_domain(note_dict: dict) -> Note:
        if not note_dict:
            return None

        if "_id" in note_dict:
            if isinstance(note_dict["_id"], Binary):
                note_id = str(note_dict["_id"].as_uuid())
            else:
                note_id = str(note_dict["_id"])
        else:
            note_id = str(note_dict.get("id"))

        return Note(
            id=Id(note_id),
            title=NoteTitle(value=note_dict["title"]),
            content=NoteContent(value=note_dict["content"]),
            user_id=note_dict["user_id"],
            created_at=note_dict["created_at"],
            updated_at=note_dict.get("updated_at"),
        )
