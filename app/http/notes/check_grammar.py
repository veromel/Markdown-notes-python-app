from fastapi import APIRouter
from pydantic import BaseModel
from src.notes.infrastructure.language_tool.language_tool import get_language_tool


class CheckGrammarRequest(BaseModel):
    content: str


async def check_grammar(request: CheckGrammarRequest):
    tool = get_language_tool()
    matches = tool.check(request.content)
    errors = [match.message for match in matches]
    return {"errors": errors}


def add_routes(router: APIRouter):
    router.get("/notes/check-grammar")(check_grammar)
