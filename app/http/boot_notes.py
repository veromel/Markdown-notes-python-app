from app.http.config import settings
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)
from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.application.update.update_note_service import UpdateNoteService
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class BootNotes:
    def __init__(self):
        self.mongo_client = None
        self.note_repository = None

    async def _initialize_mongo_client(self):
        if self.mongo_client is None:
            self.mongo_client = AsyncIOMotorClient(settings.mongodb_url)
        return self.mongo_client.notes_db

    async def _initialize_repositories(self):
        await self._initialize_mongo_client()
        self.note_repository = MongoNoteRepository()

    def _initialize_services(self):
        self.create_note_service = CreateNoteService(self.note_repository)
        self.delete_note_service = DeleteNoteService(self.note_repository)
        self.get_note_service = GetNoteByIdService(self.note_repository)
        self.list_notes_service = ListNotesService(self.note_repository)
        self.update_note_service = UpdateNoteService(self.note_repository)

    async def boot(self):
        await self._initialize_mongo_client()
        await self._initialize_repositories()
        self._initialize_services()
        return self


boot_notes_instance = BootNotes()
