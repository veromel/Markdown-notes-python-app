import inject
import traceback
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.users.domain.value_objects.id import UserId
from src.users.domain.repositories.user_repository import UserRepository
from src.users.domain.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        auth_service = inject.instance(AuthService)
        user_id = auth_service.get_user_id_from_token(token)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id
    except Exception as e:
        print(f"Error al obtener user_id del token: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error con el token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(user_id: str = Depends(get_current_user_id)):
    try:
        user_repository = inject.instance(UserRepository)
        user = await user_repository.find_by_id(UserId(user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except Exception as e:
        print(f"Error al obtener usuario actual: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error al obtener usuario: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
