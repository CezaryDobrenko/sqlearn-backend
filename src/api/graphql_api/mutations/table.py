from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.table import TableAssignmentTemplateNode, TableNode
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.table_template_service import (
    TableAssignmentTemplateManagementService,
)
from modules.database_preset.application.services.table_service import (
    TableManagementService,
)


class CreateTable(Mutation):
    table = Field(TableNode)

    class Arguments:
        database_id = ID(required=True)
        name = String(required=True)
        description = String()

    @authentication_required()
    def mutate(self, info, database_id: str, name: str, **kwargs):
        session = info.context["session"]
        database_pk = retrieve_id(database_id)
        manager = TableManagementService(session)
        table = manager.create(database_pk, name, **kwargs)
        return CreateTable(table=table)


class CreateTableAssignmentTemplate(Mutation):
    table = Field(TableAssignmentTemplateNode)

    class Arguments:
        database_assignment_template_id = ID(required=True)
        name = String(required=True)
        description = String()

    @authentication_required()
    def mutate(self, info, database_assignment_template_id: str, name: str, **kwargs):
        session = info.context["session"]
        database_assignment_template_pk = retrieve_id(database_assignment_template_id)
        manager = TableAssignmentTemplateManagementService(session)
        table = manager.create(database_assignment_template_pk, name, **kwargs)
        return CreateTableAssignmentTemplate(table=table)


class UpdateTable(Mutation):
    table = Field(TableNode)

    class Arguments:
        table_id = ID(required=True)
        name = String()
        description = String()

    @authentication_required()
    def mutate(self, info, table_id: str, **kwargs):
        session = info.context["session"]
        table_pk = retrieve_id(table_id)
        manager = TableManagementService(session)
        table = manager.update(table_pk, **kwargs)
        return UpdateTable(table=table)


class UpdateTableAssignmentTemplate(Mutation):
    table = Field(TableAssignmentTemplateNode)

    class Arguments:
        table_assignment_template_id = ID(required=True)
        name = String()
        description = String()

    @authentication_required()
    def mutate(self, info, table_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        table_assignment_template_pk = retrieve_id(table_assignment_template_id)
        manager = TableAssignmentTemplateManagementService(session)
        table = manager.update(table_assignment_template_pk, **kwargs)
        return UpdateTableAssignmentTemplate(table=table)


class RemoveTable(Mutation):
    is_removed = Boolean()

    class Arguments:
        table_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, table_id: str, **kwargs):
        session = info.context["session"]
        table_pk = retrieve_id(table_id)
        manager = TableManagementService(session)
        is_removed = manager.remove(table_pk, **kwargs)
        return RemoveTable(is_removed=is_removed)


class RemoveTableAssignmentTemplate(Mutation):
    is_removed = Boolean()

    class Arguments:
        table_assignment_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, table_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        table_assignment_template_pk = retrieve_id(table_assignment_template_id)
        manager = TableAssignmentTemplateManagementService(session)
        is_removed = manager.remove(table_assignment_template_pk, **kwargs)
        return RemoveTableAssignmentTemplate(is_removed=is_removed)


class TableMutation(ObjectType):
    create_table = CreateTable.Field()
    update_table = UpdateTable.Field()
    remove_table = RemoveTable.Field()

    create_table_assignment_template = CreateTableAssignmentTemplate.Field()
    update_table_assignment_template = UpdateTableAssignmentTemplate.Field()
    remove_table_assignment_template = RemoveTableAssignmentTemplate.Field()
