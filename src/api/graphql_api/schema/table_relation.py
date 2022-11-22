from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.database_preset.domain.models.relation import TableRelation


class TableRelationNode(SQLAlchemyObjectType):
    class Meta:
        model = TableRelation
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection


class TableRelationAssignmentTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = TableRelationAssignmentTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection
