import inject
from motor.motor_asyncio import AsyncIOMotorClient

from apps.shared.dependencies import Dependencies
from src.shared.environ import env
from src.shared.infrastructure.logger import StdoutLogger

logger = StdoutLogger()


class Boot:
    def __init__(self):
        self.mongo_client = AsyncIOMotorClient(env.MONGODB_URL)

        if not inject.is_configured():
            inject.configure(self.binder)

    def binder(self, binder):
        try:
            dependencies = Dependencies.app(
                self.mongo_client,
            )
            for dependency in dependencies:
                binder.bind(*dependency)
        except Exception as e:
            logger.critical(
                message="Unable to bind dependencies",
                code="bind_dependencies_error",
                details={"error": str(e)},
            )
            raise SystemExit from e
