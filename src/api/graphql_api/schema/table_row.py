from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.row import TableRowAssignmentTemplate

from .table_data import TableColumnDataTemplateNode


class TableRowAssignmentTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = TableRowAssignmentTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    cells = SQLAlchemyConnectionField(TableColumnDataTemplateNode)
