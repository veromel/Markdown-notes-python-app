from motor.motor_asyncio import AsyncIOMotorClient

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

        return (
            (Logger, logger),
            (NoteRepository, note_repository),
        )
