import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.assignment import AssignmentTemplate

from .database import DatabaseAssignmentTemplateNode
from .tag import AssignmentTemplateTagNode


class AssignmentTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = AssignmentTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    database = graphene.Field(DatabaseAssignmentTemplateNode)
    template_tags = SQLAlchemyConnectionField(AssignmentTemplateTagNode)
