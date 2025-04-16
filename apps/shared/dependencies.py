from motor.motor_asyncio import AsyncIOMotorClient

from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.application.update.update_note_service import UpdateNoteService
from src.notes.domain.repository import NoteRepository
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)
from src.shared.domain.logger import Logger
from src.shared.environ import env
from src.shared.infrastructure.logger import StdoutLogger


class Dependencies:
    @staticmethod
    def app(
        mongo_client: AsyncIOMotorClient,
    ) -> [tuple]:

        logger = StdoutLogger()
        note_repository = MongoNoteRepository(mongo_client, env.MONGODB_NAME)

        create_note_service = CreateNoteService(note_repository)
        delete_note_service = DeleteNoteService(note_repository)
        get_note_by_id_service = GetNoteByIdService(note_repository)
        list_notes_service = ListNotesService(note_repository)
        update_note_service = UpdateNoteService(note_repository)

        return (
            (Logger, logger),
            (NoteRepository, note_repository),
            (CreateNoteService, create_note_service),
            (DeleteNoteService, delete_note_service),
            (GetNoteByIdService, get_note_by_id_service),
            (ListNotesService, list_notes_service),
            (UpdateNoteService, update_note_service),
        )
