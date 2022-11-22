import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.assignment import AssignmentTemplate

from .database import DatabaseAssignmentTemplateNode


class AssignmentTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = AssignmentTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    database = graphene.Field(DatabaseAssignmentTemplateNode)
