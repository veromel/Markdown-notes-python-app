import inject
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.notes.domain.note import Note
from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.application.update.update_note_service import UpdateNoteService
from src.notes.infrastructure.language_tool.language_tool import get_language_tool
from apps.http.auth_middleware import get_current_user_id
from src.shared.domain.exceptions import (
    ValidationException,
    NotFoundException,
    AuthorizationException,
)

notes_router = APIRouter(prefix="/notes")


@notes_router.get("/", response_model=List[Note], status_code=200)
async def list_notes(user_id: str = Depends(get_current_user_id)):
    try:
        list_service = inject.instance(ListNotesService)
        return await list_service(user_id=user_id)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener notas: {str(e)}",
        )


@notes_router.get("/{id}", response_model=Note, status_code=200)
async def get_note(id: str, user_id: str = Depends(get_current_user_id)):
    try:
        get_service = inject.instance(GetNoteByIdService)
        note = await get_service(id)

        if note is None:
            raise NotFoundException("Nota no encontrada")

        if note.user_id != user_id:
            raise AuthorizationException("No tienes permiso para acceder a esta nota")

        return note
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la nota: {str(e)}",
        )


@notes_router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note_data: dict, user_id: str = Depends(get_current_user_id)):
    try:
        create_service = inject.instance(CreateNoteService)

        return await create_service(
            note_data.get("title", ""), note_data.get("content", ""), user_id
        )
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la nota: {str(e)}",
        )


@notes_router.put("/{id}", response_model=Note, status_code=200)
async def update_note(
    id: str, note_data: dict, user_id: str = Depends(get_current_user_id)
):
    try:
        # Primero verificamos que la nota existe
        get_service = inject.instance(GetNoteByIdService)
        existing_note = await get_service(id)

        if existing_note is None:
            raise NotFoundException("Nota no encontrada")

        if existing_note.user_id != user_id:
            raise AuthorizationException("No tienes permiso para modificar esta nota")

        update_service = inject.instance(UpdateNoteService)
        await update_service(
            id, note_data.get("title", ""), note_data.get("content", ""), user_id
        )

        updated_note = await get_service(id)
        return updated_note
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la nota: {str(e)}",
        )


@notes_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: str, user_id: str = Depends(get_current_user_id)):
    try:
        get_service = inject.instance(GetNoteByIdService)
        existing_note = await get_service(id)

        if existing_note is None:
            raise NotFoundException("Nota no encontrada")

        if existing_note.user_id != user_id:
            raise AuthorizationException("No tienes permiso para eliminar esta nota")

        delete_service = inject.instance(DeleteNoteService)
        await delete_service(id, user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la nota: {str(e)}",
        )


@notes_router.post("/{id}/check-grammar", status_code=status.HTTP_200_OK)
async def check_grammar(
    id: str, content: dict, user_id: str = Depends(get_current_user_id)
):
    try:
        get_service = inject.instance(GetNoteByIdService)
        existing_note = await get_service(id)

        if existing_note is None:
            raise NotFoundException("Nota no encontrada")

        if existing_note.user_id != user_id:
            raise AuthorizationException("No tienes permiso para revisar esta nota")

        tool = get_language_tool()
        matches = tool.check(content.get("content", ""))
        errors = [match.message for match in matches]
        return {"errors": errors}
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al revisar la gramática: {str(e)}",
        )


@notes_router.post("/check-grammar", status_code=status.HTTP_200_OK)
async def check_grammar_text(
    content: dict, user_id: str = Depends(get_current_user_id)
):
    try:
        tool = get_language_tool()
        matches = tool.check(content.get("content", ""))
        errors = [match.message for match in matches]
        return {"errors": errors}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al revisar la gramática: {str(e)}",
        )
