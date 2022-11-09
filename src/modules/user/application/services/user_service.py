from jwt_token import JWTService, TokenType
from models.utils import get_or_create, transaction_scope
from modules.user.domain.models.user import User


class UserManagementService:
    def __init__(self, session):
        self.session = session
        self.jwt_service = JWTService()

    def sign_up(self, email: str, password: str, **kwargs) -> str:
        with transaction_scope(self.session) as session:
            user, is_created = get_or_create(session, User, email=email)

            if not is_created:
                raise Exception("Email already exist!")

            user.set_password(password)
            session.add(user)

        refresh_token = self.jwt_service.create_refresh_token(user.id)
        access_token = self.jwt_service.create_authorization_token(user.id)
        return access_token, refresh_token

    def sign_in(self, email: str, password: str, **kwargs):
        with transaction_scope(self.session) as session:
            user = session.query(User).filter(User.email == email)
            if user := user.first():
                if user.check_password(password):
                    refresh_token = self.jwt_service.create_refresh_token(user.id)
                    access_token = self.jwt_service.create_authorization_token(user.id)
                    return access_token, refresh_token
        raise Exception("Invalid credentials")

    def refresh_access_token(self, refresh_token: str) -> str:
        if not refresh_token:
            raise Exception("Refresh token is not set!")

        payload = self.jwt_service.get_token_payload(
            refresh_token, TokenType.REFRESH.value
        )
        user_id = payload.get("user_id")
        return self.jwt_service.create_authorization_token(user_id)
