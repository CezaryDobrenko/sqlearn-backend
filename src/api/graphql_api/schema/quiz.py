from graphene_sqlalchemy import SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.quiz import QuizTemplate


class QuizTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = QuizTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection
