import inject
from fastapi import APIRouter, Depends, status
from typing import List

from src.notes.domain.note import Note
from src.notes.application.create.create_note_service import CreateNoteService
from src.notes.application.delete.delete_note_service import DeleteNoteService
from src.notes.application.get.get_note_by_id_service import GetNoteByIdService
from src.notes.application.get.list_notes_service import ListNotesService
from src.notes.application.update.update_note_service import UpdateNoteService
from src.notes.application.check_grammar_service import CheckGrammarService
from apps.http.auth_middleware import get_current_user_id
from src.shared.domain.exceptions import (
    ValidationException,
    NotFoundException,
    AuthorizationException,
    UnexpectedError,
)
from apps.http.exceptions.formatter import exception_responses

notes_router = APIRouter(prefix="/notes")


@notes_router.get(
    "/",
    response_model=List[Note],
    status_code=200,
    responses=exception_responses([ValidationException(), UnexpectedError()]),
)
async def list_notes(user_id: str = Depends(get_current_user_id)):
    list_service = inject.instance(ListNotesService)
    return await list_service(user_id=user_id)


@notes_router.get(
    "/{id}",
    response_model=Note,
    status_code=200,
    responses=exception_responses(
        [NotFoundException(), AuthorizationException(), UnexpectedError()]
    ),
)
async def get_note(id: str, user_id: str = Depends(get_current_user_id)):
    get_service = inject.instance(GetNoteByIdService)
    return await get_service(id, user_id)


@notes_router.post(
    "/",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    responses=exception_responses([ValidationException(), UnexpectedError()]),
)
async def create_note(note_data: dict, user_id: str = Depends(get_current_user_id)):
    create_service = inject.instance(CreateNoteService)
    return await create_service(
        note_data.get("title", ""), note_data.get("content", ""), user_id
    )


@notes_router.put(
    "/{id}",
    response_model=Note,
    status_code=200,
    responses=exception_responses(
        [
            NotFoundException(),
            ValidationException(),
            AuthorizationException(),
            UnexpectedError(),
        ]
    ),
)
async def update_note(
    id: str, note_data: dict, user_id: str = Depends(get_current_user_id)
):
    update_service = inject.instance(UpdateNoteService)
    await update_service(
        id, note_data.get("title", ""), note_data.get("content", ""), user_id
    )

    get_service = inject.instance(GetNoteByIdService)
    updated_note = await get_service(id, user_id)
    return updated_note


@notes_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=exception_responses(
        [NotFoundException(), AuthorizationException(), UnexpectedError()]
    ),
)
async def delete_note(id: str, user_id: str = Depends(get_current_user_id)):
    delete_service = inject.instance(DeleteNoteService)
    await delete_service(id, user_id)


@notes_router.post(
    "/{id}/check-grammar",
    status_code=status.HTTP_200_OK,
    responses=exception_responses(
        [
            ValidationException(),
            NotFoundException(),
            AuthorizationException(),
            UnexpectedError(),
        ]
    ),
)
async def check_grammar(
    id: str, content: dict, user_id: str = Depends(get_current_user_id)
):
    grammar_service = inject.instance(CheckGrammarService)
    errors = await grammar_service.check_note_grammar(
        id, content.get("content", ""), user_id
    )
    return {"errors": errors}


@notes_router.post(
    "/check-grammar",
    status_code=status.HTTP_200_OK,
    responses=exception_responses([ValidationException(), UnexpectedError()]),
)
async def check_grammar_text(
    content: dict, user_id: str = Depends(get_current_user_id)
):
    grammar_service = inject.instance(CheckGrammarService)
    errors = await grammar_service.check_text_grammar(content.get("content", ""))
    return {"errors": errors}
