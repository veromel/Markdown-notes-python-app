from typing import Optional
from pydantic import BaseModel, Field, field_validator, EmailStr


class UserInputDTO(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")
    name: str = Field(..., description="User name")
    user_id: Optional[str] = Field(None, description="User id")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "Contraseña123",
                "name": "Usuario Ejemplo",
            }
        }
    }


class UserOutputDTO(BaseModel):
    id: str
    email: str
    name: str
    created_at: str
    updated_at: Optional[str] = None


class LoginInputDTO(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")

    model_config = {
        "json_schema_extra": {
            "example": {"email": "usuario@ejemplo.com", "password": "Contraseña123"}
        }
    }


class LoginResponseDTO(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    user: Optional[UserOutputDTO] = Field(None, description="User info")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "email": "usuario@ejemplo.com",
                    "name": "Usuario Ejemplo",
                    "created_at": "2023-01-01T12:00:00",
                    "updated_at": "2023-01-01T12:00:00",
                },
            }
        }
    }
