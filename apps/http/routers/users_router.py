import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.users.application.dto.user_dto import (
    UserInputDTO,
    LoginInputDTO,
    UserOutputDTO,
)
from src.users.application.services.register_user import RegisterUserService
from src.users.application.services.login_user import LoginUserService
from src.shared.domain.exceptions import (
    ValidationException,
    AuthenticationException,
    UnexpectedError,
)
from apps.http.auth_middleware import get_current_user
from src.users.domain.user import User
from apps.http.exceptions.formatter import exception_responses

users_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@users_router.post(
    "/users",
    response_model=UserOutputDTO,
    status_code=status.HTTP_201_CREATED,
    responses=exception_responses(
        [ValidationException(), UnexpectedError()],
    ),
)
async def register_user(user_data: UserInputDTO):
    register_service = inject.instance(RegisterUserService)
    result = await register_service(user_data)
    return result


@users_router.post(
    "/auth/login",
    responses=exception_responses(
        [ValidationException(), AuthenticationException(), UnexpectedError()],
    ),
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    login_data = LoginInputDTO(
        email=form_data.username,  # OAuth2 usa username para el email
        password=form_data.password,
    )

    login_service = inject.instance(LoginUserService)
    result = await login_service(login_data)

    return result


@users_router.get(
    "/auth/me",
    response_model=UserOutputDTO,
    responses=exception_responses(
        [AuthenticationException(), UnexpectedError()],
    ),
)
async def get_current_user_info(user: User = Depends(get_current_user)):
    return UserOutputDTO(
        id=str(user.id.value),
        email=user.email.value,
        name=user.name,
        created_at=user.created_at.isoformat() if user.created_at else None,
        updated_at=user.updated_at.isoformat() if user.updated_at else None,
    )
