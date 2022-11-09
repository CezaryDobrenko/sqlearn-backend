from graphene import Mutation, ObjectType, String

from api.graphql_api.cookies import CookieService
from modules.user.application.services.user_service import UserManagementService


class SignUpMutation(Mutation):
    access_token = String()

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    def mutate(self, info, email: str, password: str):
        session = info.context["session"]
        manager = UserManagementService(session)
        access_token, refresh_token = manager.sign_up(email, password)
        cookie_service = CookieService(info.context)
        cookie_service.set_refresh_token(refresh_token)
        return SignUpMutation(access_token=access_token)


class SignInMutation(Mutation):
    access_token = String()

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    def mutate(self, info, email: str, password: str):
        session = info.context["session"]
        manager = UserManagementService(session)
        access_token, refresh_token = manager.sign_in(email, password)
        cookie_service = CookieService(info.context)
        cookie_service.set_refresh_token(refresh_token)
        return SignInMutation(access_token=access_token)


class RefreshTokenMutation(Mutation):
    access_token = String()

    def mutate(self, info):
        session = info.context["session"]
        cookie_service = CookieService(info.context)
        refresh_token = cookie_service.get_cookie("refresh_token")
        manager = UserManagementService(session)
        access_token = manager.refresh_access_token(refresh_token)
        return RefreshTokenMutation(access_token=access_token)


class UserMutation(ObjectType):
    sign_up = SignUpMutation.Field()
    sign_in = SignInMutation.Field()
    refresh_token = RefreshTokenMutation.Field()
