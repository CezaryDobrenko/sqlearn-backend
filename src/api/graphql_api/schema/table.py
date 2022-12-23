from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.table import Table

from .table_column import TableColumnAssignmentTemplateNode, TableColumnNode
from .table_relation import TableRelationAssignmentTemplateNode, TableRelationNode
from .table_row import TableRowAssignmentTemplateNode


class TableNode(SQLAlchemyObjectType):
    class Meta:
        model = Table
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    columns = SQLAlchemyConnectionField(TableColumnNode)
    relations = SQLAlchemyConnectionField(TableRelationNode)
    related_by = SQLAlchemyConnectionField(TableRelationNode)


class TableAssignmentTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = TableAssignmentTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    rows = SQLAlchemyConnectionField(TableRowAssignmentTemplateNode)
    columns = SQLAlchemyConnectionField(TableColumnAssignmentTemplateNode)
    relations = SQLAlchemyConnectionField(TableRelationAssignmentTemplateNode)
    related_by = SQLAlchemyConnectionField(TableRelationAssignmentTemplateNode)
