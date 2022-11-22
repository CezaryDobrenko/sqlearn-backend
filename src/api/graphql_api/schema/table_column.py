from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.database_preset.domain.models.column import TableColumn

from .table_data import TableColumnDataTemplateNode


class TableColumnNode(SQLAlchemyObjectType):
    class Meta:
        model = TableColumn
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection


class TableColumnAssignmentTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = TableColumnAssignmentTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    data = SQLAlchemyConnectionField(TableColumnDataTemplateNode)
