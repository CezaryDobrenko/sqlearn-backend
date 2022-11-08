from functools import wraps
from typing import Optional

from sqlalchemy.orm import Session

from jwt_token import JWTService, TokenType
from models import User


def login_required():
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            session = info.context["session"]
            request = info.context["request"]
            token = get_request_token(request)
            authenticated_user = get_user_by_token(session, token)
            if not authenticated_user:
                raise Exception("Unauthenticated User")
            kwargs["current_user"] = authenticated_user
            return func(root, info, *args, **kwargs)

        return wrapper

    return decorator


def get_user_by_token(session: Session, token: str) -> Optional[User]:
    jwt_service = JWTService()
    payload = jwt_service.get_token_payload(token, TokenType.AUTHORIZATION.value)
    if user_id := payload.get("user_id"):
        user = session.query(User).get(user_id)
        return user
    return None


def get_request_token(request) -> str:
    return request.headers["Authorization"].replace("Bearer ", "", 1)
