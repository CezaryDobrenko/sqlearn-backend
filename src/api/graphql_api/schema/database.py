from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.database_preset.domain.models.database import Database

from .table import TableNode


class DatabaseNode(SQLAlchemyObjectType):
    class Meta:
        model = Database
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    tables = SQLAlchemyConnectionField(TableNode)
