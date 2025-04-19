# En tests/conftest.py
import sys
import os
from pathlib import Path

import pytest
from datetime import datetime


# Añade la raíz del proyecto al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def pytest_configure():
    """Configuración global para pytest"""
    os.environ["MONGODB_URL"] = "mongodb://localhost:27017"
    os.environ["MONGODB_NAME"] = "test"
    os.environ["HOST"] = "0.0.0.0"
    os.environ["PORT"] = "8000"

    print(f"✅ Variables de entorno para tests configuradas:")
    print(f"   MONGODB_URL: {os.environ['MONGODB_URL']}")
    print(f"   MONGODB_NAME: {os.environ['MONGODB_NAME']}")


@pytest.fixture(scope="session")
def environs():
    """Fixture que proporciona acceso a las variables de entorno a través del objeto env"""
    import src.shared.environ as env_module

    env_module.env = env_module.Environment.reload()

    assert hasattr(
        env_module.env, "MONGODB_URL"
    ), "MONGODB_URL no se cargó en el objeto Environment"
    assert (
        env_module.env.MONGODB_URL == os.environ["MONGODB_URL"]
    ), "MONGODB_URL no coincide con la variable de entorno"

    return env_module.env


@pytest.fixture
def current_datetime():
    return datetime.utcnow()
