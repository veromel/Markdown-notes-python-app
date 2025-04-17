from dataclasses import dataclass
from typing import Optional


@dataclass
class UserInputDTO:
    email: str
    password: str
    name: str
    user_id: Optional[str] = None


@dataclass
class UserOutputDTO:
    id: str
    email: str
    name: str
    created_at: str
    updated_at: str


@dataclass
class LoginInputDTO:
    email: str
    password: str


@dataclass
class LoginResponseDTO:
    access_token: str
    token_type: str = "bearer"
    user: UserOutputDTO = None
