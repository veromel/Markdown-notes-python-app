from datetime import datetime
from dataclasses import dataclass, field

from src.users.domain.value_objects.id import UserId
from src.users.domain.value_objects.email import Email
from src.users.domain.value_objects.password import Password


@dataclass
class User:
    id: UserId
    email: Email
    password: Password
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = None

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = self.created_at

    def update_password(self, new_password: Password) -> None:
        self.password = new_password
        self.updated_at = datetime.now()

    def update_name(self, new_name: str) -> None:
        self.name = new_name
        self.updated_at = datetime.now()

    @staticmethod
    def create(email: str, password: str, name: str, user_id: str = None) -> "User":
        return User(
            id=UserId(user_id),
            email=Email(email),
            password=Password(password).hash(),
            name=name,
        )
