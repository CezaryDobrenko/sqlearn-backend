from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.table_relation import (
    TableRelationAssignmentTemplateNode,
    TableRelationNode,
)
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.relation_template_service import (
    TableRelationAssignmentTemplateManagementService,
)
from modules.database_preset.application.services.table_relation_service import (
    TableRelationManagementService,
)


class CreateTableRelation(Mutation):
    relation = Field(TableRelationNode)

    class Arguments:
        name = String(required=True)
        action = String(required=True)
        source_column_name = String(required=True)
        source_table_id = ID(required=True)
        relation_column_name = String(required=True)
        relation_table_id = ID(required=True)

    @authentication_required()
    def mutate(
        self,
        info,
        name: str,
        action: str,
        source_column_name: str,
        source_table_id: str,
        relation_column_name: str,
        relation_table_id: str,
        **kwargs
    ):
        session = info.context["session"]
        source_table_pk = retrieve_id(source_table_id)
        relation_table_pk = retrieve_id(relation_table_id)
        manager = TableRelationManagementService(session)
        relation = manager.create(
            source_table_pk,
            relation_table_pk,
            name,
            action,
            source_column_name,
            relation_column_name,
            **kwargs
        )
        return CreateTableRelation(relation=relation)


class UpdateTableRelation(Mutation):
    relation = Field(TableRelationNode)

    class Arguments:
        table_relation_id = ID(required=True)
        name = String()
        action = String()
        source_column_name = String()
        source_table_id = ID()
        relation_column_name = String()
        relation_table_id = ID()

    @authentication_required()
    def mutate(self, info, table_relation_id: str, **kwargs):
        session = info.context["session"]
        table_relation_pk = retrieve_id(table_relation_id)
        update = {}
        if "source_column_name" in kwargs:
            update["table_column_name"] = kwargs.pop("source_column_name")
        if "relation_column_name" in kwargs:
            update["relation_column_name"] = kwargs.pop("relation_column_name")
        if "source_table_id" in kwargs:
            source_table_id = kwargs.pop("source_table_id")
            update["table_id"] = retrieve_id(source_table_id)
        if "relation_table_id" in kwargs:
            relation_table_id = kwargs.pop("relation_table_id")
            update["relation_table_id"] = retrieve_id(relation_table_id)
        manager = TableRelationManagementService(session)
        relation = manager.update(table_relation_pk, **update | kwargs)
        return UpdateTableRelation(relation=relation)


class RemoveTableRelation(Mutation):
    is_removed = Boolean()

    class Arguments:
        table_relation_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, table_relation_id: str, **kwargs):
        session = info.context["session"]
        table_relation_pk = retrieve_id(table_relation_id)
        manager = TableRelationManagementService(session)
        is_removed = manager.remove(table_relation_pk, **kwargs)
        return RemoveTableRelation(is_removed=is_removed)


class CreateTableRelationAssignmentTemplate(Mutation):
    relation = Field(TableRelationAssignmentTemplateNode)

    class Arguments:
        name = String(required=True)
        action = String(required=True)
        source_column_name = String(required=True)
        source_table_id = ID(required=True)
        relation_column_name = String(required=True)
        relation_table_id = ID(required=True)

    @authentication_required()
    def mutate(
        self,
        info,
        name: str,
        action: str,
        source_column_name: str,
        source_table_id: str,
        relation_column_name: str,
        relation_table_id: str,
        **kwargs
    ):
        session = info.context["session"]
        source_table_pk = retrieve_id(source_table_id)
        relation_table_pk = retrieve_id(relation_table_id)
        manager = TableRelationAssignmentTemplateManagementService(session)
        relation = manager.create(
            source_table_pk,
            relation_table_pk,
            name,
            action,
            source_column_name,
            relation_column_name,
            **kwargs
        )
        return CreateTableRelationAssignmentTemplate(relation=relation)


class UpdateTableRelationAssignmentTemplate(Mutation):
    relation = Field(TableRelationAssignmentTemplateNode)

    class Arguments:
        relation_assignment_template_id = ID(required=True)
        name = String()
        action = String()
        source_column_name = String()
        source_table_id = ID()
        relation_column_name = String()
        relation_table_id = ID()

    @authentication_required()
    def mutate(self, info, relation_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        relation_assignment_template_pk = retrieve_id(relation_assignment_template_id)
        update = {}
        if "source_column_name" in kwargs:
            update["table_column_name"] = kwargs.pop("source_column_name")
        if "relation_column_name" in kwargs:
            update["relation_column_name"] = kwargs.pop("relation_column_name")
        if "source_table_id" in kwargs:
            source_table_id = kwargs.pop("source_table_id")
            update["table_id"] = retrieve_id(source_table_id)
        if "relation_table_id" in kwargs:
            relation_table_id = kwargs.pop("relation_table_id")
            update["relation_table_id"] = retrieve_id(relation_table_id)
        manager = TableRelationAssignmentTemplateManagementService(session)
        relation = manager.update(relation_assignment_template_pk, **update | kwargs)
        return UpdateTableRelationAssignmentTemplate(relation=relation)


class RemoveTableRelationAssignmentTemplate(Mutation):
    is_removed = Boolean()

    class Arguments:
        relation_assignment_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, relation_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        relation_assignment_template_pk = retrieve_id(relation_assignment_template_id)
        manager = TableRelationAssignmentTemplateManagementService(session)
        is_removed = manager.remove(relation_assignment_template_pk, **kwargs)
        return RemoveTableRelationAssignmentTemplate(is_removed=is_removed)


class TableRelationMutation(ObjectType):
    create_table_relation = CreateTableRelation.Field()
    update_table_relation = UpdateTableRelation.Field()
    remove_table_relation = RemoveTableRelation.Field()

    create_table_relation_assignment_template = (
        CreateTableRelationAssignmentTemplate.Field()
    )
    update_table_relation_assignment_template = (
        UpdateTableRelationAssignmentTemplate.Field()
    )
    remove_table_relation_assignment_template = (
        RemoveTableRelationAssignmentTemplate.Field()
    )
