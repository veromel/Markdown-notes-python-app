from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.http.boot_notes import boot_notes_instance
from app.http.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await boot_notes_instance.boot()

    yield


app = FastAPI(lifespan=lifespan)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Incluyendo el enrutador principal
app.include_router(boot_notes_instance.api_router)
