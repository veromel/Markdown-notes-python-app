from uuid import UUID
from bson import Binary

from src.users.domain.user import User
from src.users.domain.value_objects.id import UserId
from src.users.domain.value_objects.email import Email
from src.users.domain.value_objects.password import Password


class UserSchema:
    @staticmethod
    def to_mongo(user: User) -> dict:
        uuid_obj = UUID(str(user.id.value))
        binary_uuid = Binary.from_uuid(uuid_obj)

        return {
            "_id": binary_uuid,
            "email": user.email.value,
            "password": user.password.value,
            "password_is_hashed": user.password.is_hashed,
            "name": user.name,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    @staticmethod
    def to_domain(user_dict: dict) -> User:
        if not user_dict:
            return None

        if "_id" in user_dict:
            if isinstance(user_dict["_id"], Binary):
                user_id = str(user_dict["_id"].as_uuid())
            else:
                user_id = str(user_dict["_id"])
        else:
            user_id = str(user_dict.get("id"))

        return User(
            id=UserId(user_id),
            email=Email(user_dict["email"]),
            password=Password(
                value=user_dict["password"],
                is_hashed=user_dict.get("password_is_hashed", True),
            ),
            name=user_dict["name"],
            created_at=user_dict["created_at"],
            updated_at=user_dict.get("updated_at"),
        )
