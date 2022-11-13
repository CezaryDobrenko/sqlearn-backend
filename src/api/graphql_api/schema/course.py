from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course.domain.models.course import Course
from modules.course_template.domain.models.course import CourseTemplate

from .quiz import QuizTemplateNode


class CourseNode(SQLAlchemyObjectType):
    class Meta:
        model = Course
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection


class CourseTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = CourseTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    quiz_templates = SQLAlchemyConnectionField(QuizTemplateNode)
