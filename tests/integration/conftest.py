import asyncio
import datetime
import uuid
import os
from pathlib import Path

import pytest
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="session")
def database_name():
    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"test_notes_{timestamp}_{unique_id}"


@pytest.fixture(scope="session")
async def mongo_client(environs):
    """Crea un cliente MongoDB para los tests"""
    try:
        mongodb_url = environs.MONGODB_URL
    except AttributeError:
        mongodb_url = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")

    client = AsyncIOMotorClient(
        mongodb_url,
        uuidRepresentation="standard",
        serverSelectionTimeoutMS=5000,
        maxPoolSize=50,
        minPoolSize=10,
        maxIdleTimeMS=30000,
        waitQueueTimeoutMS=5000,
    )

    try:
        await client.admin.command("ping")
        print("✅ Conexión a MongoDB establecida correctamente")
    except Exception as e:
        pytest.fail(f"❌ No se pudo conectar a MongoDB: {e}")

    yield client
    client.close()


@pytest.fixture
async def default_mongo_database(mongo_client, database_name):
    test_db_name = f"{database_name}_{uuid.uuid4().hex[:6]}"
    print(f"Usando base de datos: {test_db_name}")

    await mongo_client.drop_database(test_db_name)

    yield test_db_name

    print(f"Limpiando base de datos: {test_db_name}")
    await mongo_client.drop_database(test_db_name)
