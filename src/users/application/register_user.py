from datetime import datetime
import inject
import traceback

from src.users.domain.user import User
from src.users.domain.value_objects.email import Email
from src.users.domain.repositories.user_repository import UserRepository
from src.users.application.dto.user_dto import UserInputDTO, UserOutputDTO
from src.shared.domain.exceptions import ValidationException


class RegisterUserService:
    @inject.autoparams()
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, input_dto: UserInputDTO) -> UserOutputDTO:
        try:
            existing_user = await self.user_repository.find_by_email(
                Email(input_dto.email)
            )
            if existing_user:
                raise ValidationException("Ya existe un usuario con ese email")

            user = User.create(
                email=input_dto.email,
                password=input_dto.password,
                name=input_dto.name,
                user_id=input_dto.user_id,
            )

            await self.user_repository.save(user)

            return UserOutputDTO(
                id=str(user.id.value),
                email=user.email.value,
                name=user.name,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat(),
            )
        except ValidationException:
            raise
        except Exception as e:
            print(f"Error en RegisterUserService: {str(e)}")
            print(traceback.format_exc())
            raise
