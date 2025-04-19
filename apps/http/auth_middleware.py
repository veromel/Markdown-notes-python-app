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
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id
    except Exception as e:
        print(f"Error getting user_id from token: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error with token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(user_id: str = Depends(get_current_user_id)):
    try:
        user_repository = inject.instance(UserRepository)
        user = await user_repository.find_by_id(UserId(user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except Exception as e:
        print(f"Error getting current user: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error getting user: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
