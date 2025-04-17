from motor.motor_asyncio import AsyncIOMotorClient

from src.shared.environ import env


class MongoClient:
    def __new__(cls) -> AsyncIOMotorClient:
        try:
            client = AsyncIOMotorClient(
                env.MONGODB_URL,
                uuidRepresentation="standard",
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=30000,
                waitQueueTimeoutMS=5000,
            )
            # logger.info(
            #     message="MongoDb connected successfully",
            #     code="mongodb_connected",
            # )
        except Exception as e:
            # logger.critical(
            #     message="Unable to connect to MongoDb",
            #     code="mongodb_connection_error",
            #     details={"error": str(e)},
            # )
            raise SystemExit from e
        else:
            return client
