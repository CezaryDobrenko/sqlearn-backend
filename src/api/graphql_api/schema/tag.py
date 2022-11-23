from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.assignment_tag import AssignmentTemplateTag
from modules.course_template.domain.models.tag import Tag


class TagNode(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection


class AssignmentTemplateTagNode(SQLAlchemyObjectType):
    class Meta:
        model = AssignmentTemplateTag
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection
