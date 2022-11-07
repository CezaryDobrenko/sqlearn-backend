import enum
import time

import jwt

from config import Config


class TokenType(enum.Enum):
    AUTHORIZATION = "AUTHORIZATION"
    REFRESH = "REFRESH"


class JWTService:
    secret: str
    algorithm: str
    expire_time: int
    refresh_expire_time: int

    def __init__(self):
        self.secret = Config.JWT_SECRET
        self.algorithm = Config.JWT_ALGORITHM
        self.expire_time = Config.JWT_EXPIRE_TIME
        self.refresh_expire_time = Config.JWT_REFRESH_EXPIRE_TIME

    def create_authorization_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "token_type": TokenType.AUTHORIZATION.value,
            "exp": time.time() + self.expire_time,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "token_type": TokenType.REFRESH.value,
            "exp": time.time() + self.refresh_expire_time,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> bool:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])
