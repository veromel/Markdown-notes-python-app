from motor.motor_asyncio import AsyncIOMotorClient

from src.notes.domain.repository import NoteRepository
from src.notes.infrastructure.repositories.mongo_note_repository import (
    MongoNoteRepository,
)
from src.shared.domain.logger import Logger
from src.shared.environ import env
from src.shared.infrastructure.logger import StdoutLogger

from src.users.domain.repositories.user_repository import UserRepository
from src.users.domain.services.auth_service import AuthService
from src.users.infrastructure.repositories.mongo_user_repository import (
    MongoUserRepository,
)
from src.users.infrastructure.services.jwt_auth_service import JWTAuthService


class Dependencies:
    @staticmethod
    def app(
        mongo_client: AsyncIOMotorClient,
    ) -> [tuple]:
        # Mapeo de las implementaciones de infraestructura
        logger = StdoutLogger()
        note_repository = MongoNoteRepository(mongo_client, env.MONGODB_NAME)
        user_repository = MongoUserRepository(mongo_client, env.MONGODB_NAME)
        auth_service = JWTAuthService()

        return (
            (Logger, logger),
            (NoteRepository, note_repository),
            (UserRepository, user_repository),
            (AuthService, auth_service),
        )
