from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.quiz import QuizTemplateNode
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.quiz_template_service import (
    QuizTemplateManagementService,
)


class CreateQuizTemplate(Mutation):
    quiz_template = Field(QuizTemplateNode)

    class Arguments:
        course_template_id = ID(required=True)
        title = String(required=True)
        description = String()

    @authentication_required()
    def mutate(self, info, course_template_id: str, title: str, **kwargs):
        session = info.context["session"]
        course_template_pk = retrieve_id(course_template_id)
        manager = QuizTemplateManagementService(session)
        quiz_template = manager.create(course_template_pk, title, **kwargs)
        return CreateQuizTemplate(quiz_template=quiz_template)


class UpdateQuizTemplate(Mutation):
    course_template = Field(QuizTemplateNode)

    class Arguments:
        quiz_template_id = ID(required=True)
        title = String()
        description = String()

    @authentication_required()
    def mutate(self, info, quiz_template_id: str, **kwargs):
        session = info.context["session"]
        quiz_template_pk = retrieve_id(quiz_template_id)
        manager = QuizTemplateManagementService(session)
        course_template = manager.update(quiz_template_pk, **kwargs)
        return UpdateQuizTemplate(course_template=course_template)


class RemoveQuizTemplate(Mutation):
    is_removed = Boolean()

    class Arguments:
        quiz_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, quiz_template_id: str, **kwargs):
        session = info.context["session"]
        quiz_template_pk = retrieve_id(quiz_template_id)
        manager = QuizTemplateManagementService(session)
        is_removed = manager.remove(quiz_template_pk, **kwargs)
        return RemoveQuizTemplate(is_removed=is_removed)


class QuizMutation(ObjectType):
    create_course_template = CreateQuizTemplate.Field()
    update_course_template = UpdateQuizTemplate.Field()
    remove_course_template = RemoveQuizTemplate.Field()
