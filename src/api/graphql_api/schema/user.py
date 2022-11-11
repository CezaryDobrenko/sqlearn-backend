from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from models import User

from .course import CourseTemplateNode


class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (AuthorizedNode,)
        exclude_fields = {"password"}
        connection_class = ExtendedConnection

    course_templates = SQLAlchemyConnectionField(CourseTemplateNode)
