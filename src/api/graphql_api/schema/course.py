from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from modules.quiz.domain.models.course import CourseTemplate


class CourseTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = CourseTemplate
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
