import inject
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.users.application.dto.user_dto import (
    UserInputDTO,
    LoginInputDTO,
    UserOutputDTO,
)
from src.users.application.register_user import RegisterUserService
from src.users.application.login_user import LoginUserService
from src.shared.domain.exceptions import ValidationException
from apps.http.auth_middleware import get_current_user
from src.users.domain.user import User

users_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@users_router.post("/users", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserInputDTO):
    try:
        register_service = inject.instance(RegisterUserService)
        result = await register_service(user_data)
        return result
    except ValidationException as e:
        print(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error al registrar usuario: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}",
        )


@users_router.post("/auth/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        login_data = LoginInputDTO(
            email=form_data.username,  # OAuth2 usa username para el email
            password=form_data.password,
        )

        login_service = inject.instance(LoginUserService)
        result = await login_service(login_data)

        return {
            "access_token": result.access_token,
            "token_type": result.token_type,
            "user": {
                "id": result.user.id,
                "email": result.user.email,
                "name": result.user.name,
            },
        }
    except ValidationException as e:
        print(f"Error de validación en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Error al iniciar sesión: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar sesión: {str(e)}",
        )


@users_router.get("/auth/me", response_model=dict)
async def get_current_user_info(user: User = Depends(get_current_user)):
    try:
        return {
            "id": str(user.id.value),
            "email": user.email.value,
            "name": user.name,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
    except Exception as e:
        print(f"Error al obtener información del usuario: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener información del usuario: {str(e)}",
        )
