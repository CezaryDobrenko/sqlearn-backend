from graphene.relay.node import to_global_id

from models import User
from models.base_model import BaseModel
from tests.conftest import JWTService, RequestFactory


def gid(obj: BaseModel) -> str:
    class_name = f"{obj.__class__.__name__}Node"
    return to_global_id(class_name, obj.id)


def authenticated_request(user: User) -> str:
    jwt_service = JWTService()
    request_factory = RequestFactory()
    auth_token = jwt_service.create_authorization_token(user.id)
    return request_factory(headers={"Authorization": f"Bearer {auth_token}"})
