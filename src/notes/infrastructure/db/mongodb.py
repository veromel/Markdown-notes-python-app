from motor.motor_asyncio import AsyncIOMotorClient


def get_mongo_client(mongo_url: str):
    return AsyncIOMotorClient(mongo_url)
