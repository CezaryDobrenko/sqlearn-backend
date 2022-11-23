from graphene import ID, Boolean, Field, Mutation, ObjectType

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.tag import AssignmentTemplateTagNode
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.assignment_template_tag_service import (
    AssignmentTemplateTagManagementService,
)


class CreateAssignmentTemplateTag(Mutation):
    assignment_template_tag = Field(AssignmentTemplateTagNode)

    class Arguments:
        assignment_template_id = ID(required=True)
        tag_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, assignment_template_id: str, tag_id: str, **kwargs):
        session = info.context["session"]
        assignment_template_pk = retrieve_id(assignment_template_id)
        tag_pk = retrieve_id(tag_id)
        manager = AssignmentTemplateTagManagementService(session)
        assignment_template_tag = manager.create(
            assignment_template_pk, tag_pk, **kwargs
        )
        return CreateAssignmentTemplateTag(
            assignment_template_tag=assignment_template_tag
        )


class RemoveAssignmentTemplateTag(Mutation):
    is_removed = Boolean()

    class Arguments:
        assignment_template_tag_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, assignment_template_tag_id: str, **kwargs):
        session = info.context["session"]
        assignment_template_tag_pk = retrieve_id(assignment_template_tag_id)
        manager = AssignmentTemplateTagManagementService(session)
        is_removed = manager.remove(assignment_template_tag_pk, **kwargs)
        return RemoveAssignmentTemplateTag(is_removed=is_removed)


class AssignmentTemplateTagMutation(ObjectType):
    create_assignment_template_tag = CreateAssignmentTemplateTag.Field()
    remove_assignment_template_tag = RemoveAssignmentTemplateTag.Field()
