from fastapi import APIRouter
from pydantic import BaseModel
from src.notes.infrastructure.language_tool.language_tool import get_language_tool

api_router = APIRouter()


class CheckGrammarRequest(BaseModel):
    content: str


@api_router.post("/check-grammar")
async def check_grammar(request: CheckGrammarRequest):
    tool = get_language_tool()
    matches = tool.check(request.content)
    errors = [match.message for match in matches]
    return {"errors": errors}
