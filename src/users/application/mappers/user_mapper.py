from src.users.domain.user import User
from src.users.domain.value_objects.email import Email
from src.users.application.dto.user_dto import (
    UserInputDTO,
    UserOutputDTO,
    LoginInputDTO,
)


class UserMapper:
    @staticmethod
    def to_domain(dto: UserInputDTO) -> User:
        return User.create(
            email=dto.email, password=dto.password, name=dto.name, user_id=dto.user_id
        )

    @staticmethod
    def to_dto(user: User) -> UserOutputDTO:
        return UserOutputDTO(
            id=str(user.id.value),
            email=user.email.value,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat() if user.updated_at else None,
        )

    @staticmethod
    def login_to_domain(dto: LoginInputDTO) -> (Email, str):
        return Email(dto.email), dto.password
