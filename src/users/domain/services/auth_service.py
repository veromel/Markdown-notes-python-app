from abc import ABC, abstractmethod
from typing import Dict, Optional

from src.users.domain.user import User


class AuthService(ABC):
    @abstractmethod
    def generate_token(self, user: User) -> str:
        pass

    @abstractmethod
    def validate_token(self, token: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_user_id_from_token(self, token: str) -> Optional[str]:
        pass
