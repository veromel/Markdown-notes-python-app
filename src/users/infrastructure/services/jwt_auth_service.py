import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional

from src.users.domain.user import User
from src.users.domain.services.auth_service import AuthService
from src.shared.environ import env


class JWTAuthService(AuthService):
    def __init__(self):
        self.secret_key = getattr(
            env, "JWT_SECRET_KEY", "default_secret_key_change_in_production"
        )
        self.algorithm = "HS256"
        self.token_expire_minutes = int(
            getattr(env, "JWT_EXPIRE_MINUTES", 1440)
        )  # 24 horas por defecto

    def generate_token(self, user: User) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)

        payload = {
            "sub": str(user.id.value),
            "email": user.email.value,
            "name": user.name,
            "exp": expire,
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return token

    def validate_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None

    def get_user_id_from_token(self, token: str) -> Optional[str]:
        payload = self.validate_token(token)
        if not payload:
            return None

        return payload.get("sub")
