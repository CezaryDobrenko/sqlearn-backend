from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.course import CourseTemplateNode
from api.graphql_api.utils import retrieve_id
from modules.quiz.application.services.course_template_service import (
    CourseTemplateManagementService,
)


class CreateCourseTemplate(Mutation):
    course_template = Field(CourseTemplateNode)

    class Arguments:
        name = String(required=True)
        description = String()
        is_public = Boolean()

    @authentication_required()
    def mutate(self, info, name: str, **kwargs):
        session = info.context["session"]
        manager = CourseTemplateManagementService(session)
        course_template = manager.create(name, **kwargs)
        return CreateCourseTemplate(course_template=course_template)


class UpdateCourseTemplate(Mutation):
    course_template = Field(CourseTemplateNode)

    class Arguments:
        course_template_id = ID(required=True)
        name = String()
        description = String()
        is_public = Boolean()

    @authentication_required()
    def mutate(self, info, course_template_id: str, **kwargs):
        session = info.context["session"]
        course_template_pk = retrieve_id(course_template_id)
        manager = CourseTemplateManagementService(session)
        course_template = manager.update(course_template_pk, **kwargs)
        return UpdateCourseTemplate(course_template=course_template)


class RemoveCourseTemplate(Mutation):
    is_removed = Boolean()

    class Arguments:
        course_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, course_template_id: str, **kwargs):
        session = info.context["session"]
        course_template_pk = retrieve_id(course_template_id)
        manager = CourseTemplateManagementService(session)
        is_removed = manager.remove(course_template_pk, **kwargs)
        return RemoveCourseTemplate(is_removed=is_removed)


class PublishCourseTemplate(Mutation):
    is_published = Boolean()

    class Arguments:
        course_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, course_template_id: str, **kwargs):
        session = info.context["session"]
        course_template_pk = retrieve_id(course_template_id)
        manager = CourseTemplateManagementService(session)
        is_published = manager.publish(course_template_pk, **kwargs)
        return PublishCourseTemplate(is_published=is_published)


class WithdrawCourseTemplate(Mutation):
    is_withdrawed = Boolean()

    class Arguments:
        course_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, course_template_id: str, **kwargs):
        session = info.context["session"]
        course_template_pk = retrieve_id(course_template_id)
        manager = CourseTemplateManagementService(session)
        is_withdrawed = manager.withdraw(course_template_pk, **kwargs)
        return WithdrawCourseTemplate(is_withdrawed=is_withdrawed)


class CourseMutation(ObjectType):
    create_course_template = CreateCourseTemplate.Field()
    update_course_template = UpdateCourseTemplate.Field()
    remove_course_template = RemoveCourseTemplate.Field()
    publish_course_template = PublishCourseTemplate.Field()
    withdraw_course_template = WithdrawCourseTemplate.Field()
