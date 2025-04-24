import inject

from src.users.application.dto.user_dto import UserInputDTO, UserOutputDTO
from src.users.application.mappers.user_mapper import UserMapper
from src.users.domain.repositories.user_repository import UserRepository
from src.users.domain.value_objects.email import Email
from src.shared.domain.exceptions import ValidationException


class RegisterUserService:
    @inject.autoparams()
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, input_dto: UserInputDTO) -> UserOutputDTO:
        existing_user = await self.user_repository.find_by_email(Email(input_dto.email))
        if existing_user:
            raise ValidationException(detail="A user with this email already exists")

        user = UserMapper.to_domain(input_dto)

        await self.user_repository.save(user)

        return UserMapper.to_dto(user)
