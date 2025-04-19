import inject
import traceback
from src.users.domain.value_objects.email import Email
from src.users.domain.repositories.user_repository import UserRepository
from src.users.domain.services.auth_service import AuthService
from src.users.application.dto.user_dto import (
    LoginInputDTO,
    LoginResponseDTO,
    UserOutputDTO,
)
from src.shared.domain.exceptions import ValidationException


class LoginUserService:
    @inject.autoparams()
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def __call__(self, input_dto: LoginInputDTO) -> LoginResponseDTO:
        try:
            user = await self.user_repository.find_by_email(Email(input_dto.email))
            if not user:
                raise ValidationException("Wrong credentials")

            if not user.password.check(input_dto.password):
                raise ValidationException("Wrong credentials")

            token = self.auth_service.generate_token(user)

            return LoginResponseDTO(
                access_token=token,
                token_type="bearer",
                user=UserOutputDTO(
                    id=str(user.id.value),
                    email=user.email.value,
                    name=user.name,
                    created_at=user.created_at.isoformat(),
                    updated_at=user.updated_at.isoformat() if user.updated_at else None,
                ),
            )
        except ValidationException:
            raise
        except Exception as e:
            print(f"Error in LoginUserService: {str(e)}")
            print(traceback.format_exc())
            raise
