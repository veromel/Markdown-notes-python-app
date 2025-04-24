import inject

from src.users.application.dto.user_dto import LoginInputDTO, LoginResponseDTO
from src.users.application.mappers.user_mapper import UserMapper
from src.users.domain.repositories.user_repository import UserRepository
from src.users.domain.services.auth_service import AuthService
from src.users.domain.value_objects.email import Email
from src.shared.domain.exceptions import AuthenticationException


class LoginUserService:
    @inject.autoparams()
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def __call__(self, input_dto: LoginInputDTO) -> LoginResponseDTO:
        user = await self.user_repository.find_by_email(Email(input_dto.email))
        if not user:
            raise AuthenticationException(detail="Invalid credentials")

        if not user.password.check(input_dto.password):
            raise AuthenticationException(detail="Invalid credentials")

        token = self.auth_service.generate_token(user)

        return LoginResponseDTO(
            access_token=token, token_type="bearer", user=UserMapper.to_dto(user)
        )
