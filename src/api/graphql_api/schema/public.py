import graphene
from graphene.relay.node import to_global_id
from graphene_sqlalchemy import SQLAlchemyConnectionField

from modules.course_template.domain.models.course import CourseTemplate

from .course import CourseTemplateNode


class Public(graphene.ObjectType):
    id = graphene.ID()
    avalible_courses = SQLAlchemyConnectionField(CourseTemplateNode)

    def resolve_avalible_courses(self, info, **kwargs):
        session = info.context["session"]
        avalible_courses = session.query(CourseTemplate).filter(
            CourseTemplate.is_public.is_(True), CourseTemplate.is_published.is_(True)
        )
        return avalible_courses


class PublicQuery(graphene.ObjectType):
    public = graphene.Field(Public)

    def resolve_public(self, info):
        return Public(id=to_global_id("Public", 1))
