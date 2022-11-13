from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.database_preset.domain.models.column import TableColumn


class TableColumnNode(SQLAlchemyObjectType):
    class Meta:
        model = TableColumn
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection
