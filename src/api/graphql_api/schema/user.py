from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from models import User


class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        exclude_fields = {"password"}
        connection_class = ExtendedConnection
