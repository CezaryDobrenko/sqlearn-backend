import graphene
from graphene.relay.node import to_global_id
from graphene_sqlalchemy import SQLAlchemyConnectionField

from modules.course_template.domain.models.course import CourseTemplate
from modules.database_preset.domain.models.column import ColumnType
from modules.database_preset.domain.models.database import Database

from .course import CourseTemplateNode
from .database import DatabaseNode


class Public(graphene.ObjectType):
    id = graphene.ID()
    avalible_courses = SQLAlchemyConnectionField(CourseTemplateNode)
    databases = SQLAlchemyConnectionField(DatabaseNode)
    column_types = graphene.List(graphene.String)

    def resolve_avalible_courses(self, info, **kwargs):
        session = info.context["session"]
        avalible_courses = session.query(CourseTemplate).filter(
            CourseTemplate.is_public.is_(True), CourseTemplate.is_published.is_(True)
        )
        return avalible_courses

    def resolve_databases(self, info, **kwargs):
        session = info.context["session"]
        databases = session.query(Database).filter(Database.user_id.is_(None))
        return databases

    def resolve_column_types(self, info, **kwargs):
        return [column.value for column in ColumnType]


class PublicQuery(graphene.ObjectType):
    public = graphene.Field(Public)

    def resolve_public(self, info):
        return Public(id=to_global_id("Public", 1))
