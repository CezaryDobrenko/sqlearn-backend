from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.assignment import AssignmentTemplateNode
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.assignment_template_service import (
    AssignmentTemplateManagementService,
)


class CreateAssignmentTemplate(Mutation):
    assignment_template = Field(AssignmentTemplateNode)

    class Arguments:
        quiz_template_id = ID(required=True)
        title = String(required=True)
        database_id = ID()
        description = String()
        owner_solution = String()

    @authentication_required()
    def mutate(self, info, quiz_template_id: str, title: str, **kwargs):
        session = info.context["session"]
        quiz_template_pk = retrieve_id(quiz_template_id)
        database_pk = (
            retrieve_id(kwargs.pop("database_id", None))
            if "database_id" in kwargs
            else None
        )
        manager = AssignmentTemplateManagementService(session)
        assignment_template = manager.create(
            quiz_template_pk, title, database_pk, **kwargs
        )
        return CreateAssignmentTemplate(assignment_template=assignment_template)


class UpdateAssignmentTemplate(Mutation):
    assignment_template = Field(AssignmentTemplateNode)

    class Arguments:
        assignment_template_id = ID(required=True)
        title = String()
        database_id = ID()
        description = String()
        owner_solution = String()

    @authentication_required()
    def mutate(self, info, assignment_template_id: str, **kwargs):
        session = info.context["session"]
        assignment_template_pk = retrieve_id(assignment_template_id)
        database_pk = (
            retrieve_id(kwargs.pop("database_id", None))
            if "database_id" in kwargs
            else None
        )
        manager = AssignmentTemplateManagementService(session)
        assignment_template = manager.update(
            assignment_template_pk, database_pk, **kwargs
        )
        return UpdateAssignmentTemplate(assignment_template=assignment_template)


class RemoveAssignmentTemplate(Mutation):
    is_removed = Boolean()

    class Arguments:
        assignment_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, assignment_template_id: str, **kwargs):
        session = info.context["session"]
        assignment_template_pk = retrieve_id(assignment_template_id)
        manager = AssignmentTemplateManagementService(session)
        is_removed = manager.remove(assignment_template_pk, **kwargs)
        return RemoveAssignmentTemplate(is_removed=is_removed)


class AssignmentTemplateMutation(ObjectType):
    create_assignment_template = CreateAssignmentTemplate.Field()
    update_assignment_template = UpdateAssignmentTemplate.Field()
    remove_assignment_template = RemoveAssignmentTemplate.Field()
