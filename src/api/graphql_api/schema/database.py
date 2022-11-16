from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.database_preset.domain.models.database import Database
from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table

from .table import TableNode
from .table_relation import TableRelationNode


class DatabaseNode(SQLAlchemyObjectType):
    class Meta:
        model = Database
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    tables = SQLAlchemyConnectionField(TableNode)
    relations = SQLAlchemyConnectionField(TableRelationNode)

    def resolve_relations(self, info, **kwargs):
        return self.tables.join(
            TableRelation, Table.id == TableRelation.table_id
        ).with_entities(TableRelation)
