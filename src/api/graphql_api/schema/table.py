from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.database_preset.domain.models.table import Table

from .table_column import TableColumnNode
from .table_relation import TableRelationNode


class TableNode(SQLAlchemyObjectType):
    class Meta:
        model = Table
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    columns = SQLAlchemyConnectionField(TableColumnNode)
    relations = SQLAlchemyConnectionField(TableRelationNode)
