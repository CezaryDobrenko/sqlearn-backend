from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.quiz.domain.models.course import CourseTemplate


class CourseTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = CourseTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection
