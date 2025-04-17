from abc import ABC, abstractmethod
from typing import Optional

from src.users.domain.user import User
from src.users.domain.value_objects.id import UserId
from src.users.domain.value_objects.email import Email


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, id: UserId) -> None:
        pass
