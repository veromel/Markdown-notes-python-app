from typing import Optional
import traceback

from motor.motor_asyncio import AsyncIOMotorClient

from src.users.domain.user import User
from src.users.domain.value_objects.id import UserId
from src.users.domain.value_objects.email import Email
from src.users.domain.repositories.user_repository import UserRepository
from src.users.infrastructure.repositories.schema import UserSchema


class MongoUserRepository(UserRepository):
    def __init__(self, client: AsyncIOMotorClient, mongodb_name: str):
        self.database = client[mongodb_name]
        self.collection = self.database["users"]
        self.schema = UserSchema()

    async def save(self, user: User) -> None:
        try:
            user_dict = UserSchema.to_mongo(user)

            result = await self.collection.replace_one(
                {"_id": user_dict["_id"]}, user_dict, upsert=True
            )
        except Exception as e:
            print(f"Error al guardar usuario: {str(e)}")
            print(traceback.format_exc())
            raise e

    async def find_by_id(self, id: UserId) -> Optional[User]:
        try:
            from uuid import UUID
            from bson import Binary

            uuid_obj = UUID(str(id.value))
            binary_uuid = Binary.from_uuid(uuid_obj)

            user_dict = await self.collection.find_one({"_id": binary_uuid})
            return UserSchema.to_domain(user_dict) if user_dict else None
        except Exception as e:
            print(f"Error al buscar usuario por ID: {str(e)}")
            print(traceback.format_exc())
            return None

    async def find_by_email(self, email: Email) -> Optional[User]:
        try:
            user_dict = await self.collection.find_one({"email": email.value})
            return UserSchema.to_domain(user_dict) if user_dict else None
        except Exception as e:
            print(f"Error al buscar usuario por email: {str(e)}")
            print(traceback.format_exc())
            return None

    async def delete(self, id: UserId) -> None:
        try:
            from uuid import UUID
            from bson import Binary

            uuid_obj = UUID(str(id.value))
            binary_uuid = Binary.from_uuid(uuid_obj)

            await self.collection.delete_one({"_id": binary_uuid})
        except Exception as e:
            print(f"Error al eliminar usuario: {str(e)}")
            print(traceback.format_exc())
            raise e
