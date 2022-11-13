from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from sqlalchemy import or_

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from models import User
from modules.database_preset.domain.models.database import Database

from .course import CourseNode, CourseTemplateNode
from .database import DatabaseNode


class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (AuthorizedNode,)
        exclude_fields = {"password"}
        connection_class = ExtendedConnection

    courses = SQLAlchemyConnectionField(CourseNode)
    course_templates = SQLAlchemyConnectionField(CourseTemplateNode)
    databases = SQLAlchemyConnectionField(DatabaseNode)

    def resolve_databases(self, info, **kwargs):
        session = info.context["session"]
        databases = session.query(Database).filter(
            or_(Database.user_id.is_(None), Database.user_id == self.id)
        )
        return databases
