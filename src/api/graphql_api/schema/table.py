from graphene import ObjectType, relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.table import Table

from .table_column import TableColumnAssignmentTemplateNode, TableColumnNode
from .table_data import TableColumnDataTemplateNode
from .table_relation import TableRelationAssignmentTemplateNode, TableRelationNode


class TableRowNode(ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    cells = SQLAlchemyConnectionField(TableColumnDataTemplateNode)

    @classmethod
    def from_template(cls, table_template: TableAssignmentTemplate):
        column_count = table_template.columns.count()
        data_set = (
            table_template.columns.join(TableColumnDataTemplate)
            .with_entities(TableColumnDataTemplate)
            .all()
        )
        return [
            cls(
                id=f"{table_template.id}.{i}.table_assignment_template",
                ceils=data_set[i: i + column_count],
            )
            for i in range(0, len(data_set), column_count)
        ]


class TableRowConnection(relay.Connection):
    class Meta:
        node = TableRowNode


class TableNode(SQLAlchemyObjectType):
    class Meta:
        model = Table
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    columns = SQLAlchemyConnectionField(TableColumnNode)
    relations = SQLAlchemyConnectionField(TableRelationNode)


class TableAssignmentTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = TableAssignmentTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    rows = relay.ConnectionField(TableRowConnection)
    columns = SQLAlchemyConnectionField(TableColumnAssignmentTemplateNode)
    relations = SQLAlchemyConnectionField(TableRelationAssignmentTemplateNode)

    def resolve_rows(self, info, **kwargs):
        return TableRowNode.from_template(self)
