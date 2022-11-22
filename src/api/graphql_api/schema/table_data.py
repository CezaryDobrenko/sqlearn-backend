from graphene import String
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.column_data import TableColumnDataTemplate


class TableColumnDataTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = TableColumnDataTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    column = String()

    def resolve_column(self, info, **kwargs):
        return self.table_column_assignment_template.name
