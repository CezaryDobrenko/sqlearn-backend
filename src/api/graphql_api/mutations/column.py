from graphene import ID, Boolean, Field, Int, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.table_column import (
    TableColumnAssignmentTemplateNode,
    TableColumnNode,
)
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.column_template_service import (
    ColumnAssignmentTemplateManagementService,
)
from modules.database_preset.application.services.table_column_service import (
    TableColumnManagementService,
)


class CreateTableColumn(Mutation):
    column = Field(TableColumnNode)

    class Arguments:
        table_id = ID(required=True)
        name = String(required=True)
        type = String(required=True)
        length = Int()
        is_null = Boolean()
        is_unique = Boolean()

    @authentication_required()
    def mutate(self, info, table_id: str, name: str, type: str, **kwargs):
        session = info.context["session"]
        table_pk = retrieve_id(table_id)
        manager = TableColumnManagementService(session)
        column = manager.create(table_pk, name, type, **kwargs)
        return CreateTableColumn(column=column)


class UpdateTableColumn(Mutation):
    column = Field(TableColumnNode)

    class Arguments:
        table_column_id = ID(required=True)
        name = String()
        type = String()
        length = Int()
        is_null = Boolean()
        is_unique = Boolean()

    @authentication_required()
    def mutate(self, info, table_column_id: str, **kwargs):
        session = info.context["session"]
        table_column_pk = retrieve_id(table_column_id)
        manager = TableColumnManagementService(session)
        column = manager.update(table_column_pk, **kwargs)
        return UpdateTableColumn(column=column)


class RemoveTableColumn(Mutation):
    is_removed = Boolean()

    class Arguments:
        table_column_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, table_column_id: str, **kwargs):
        session = info.context["session"]
        table_column_pk = retrieve_id(table_column_id)
        manager = TableColumnManagementService(session)
        is_removed = manager.remove(table_column_pk, **kwargs)
        return RemoveTableColumn(is_removed=is_removed)


class CreateTableColumnAssignmentTemplate(Mutation):
    column = Field(TableColumnAssignmentTemplateNode)

    class Arguments:
        table_assignment_template_id = ID(required=True)
        name = String(required=True)
        type = String(required=True)
        length = Int()
        is_null = Boolean()
        is_unique = Boolean()

    @authentication_required()
    def mutate(
        self, info, table_assignment_template_id: str, name: str, type: str, **kwargs
    ):
        session = info.context["session"]
        table_assignment_template_pk = retrieve_id(table_assignment_template_id)
        manager = ColumnAssignmentTemplateManagementService(session)
        column = manager.create(table_assignment_template_pk, name, type, **kwargs)
        return CreateTableColumnAssignmentTemplate(column=column)


class UpdateTableColumnAssignmentTemplate(Mutation):
    column = Field(TableColumnAssignmentTemplateNode)

    class Arguments:
        column_assignment_template_id = ID(required=True)
        name = String()
        type = String()
        length = Int()
        is_null = Boolean()
        is_unique = Boolean()

    @authentication_required()
    def mutate(self, info, column_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        column_assignment_template_pk = retrieve_id(column_assignment_template_id)
        manager = ColumnAssignmentTemplateManagementService(session)
        column = manager.update(column_assignment_template_pk, **kwargs)
        return UpdateTableColumnAssignmentTemplate(column=column)


class RemoveTableColumnAssignmentTemplate(Mutation):
    is_removed = Boolean()

    class Arguments:
        column_assignment_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, column_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        column_assignment_template_pk = retrieve_id(column_assignment_template_id)
        manager = ColumnAssignmentTemplateManagementService(session)
        is_removed = manager.remove(column_assignment_template_pk, **kwargs)
        return RemoveTableColumnAssignmentTemplate(is_removed=is_removed)


class TableColumnMutation(ObjectType):
    create_table_column = CreateTableColumn.Field()
    update_table_column = UpdateTableColumn.Field()
    remove_table_column = RemoveTableColumn.Field()

    create_table_column_assignment_template = (
        CreateTableColumnAssignmentTemplate.Field()
    )
    update_table_column_assignment_template = (
        UpdateTableColumnAssignmentTemplate.Field()
    )
    remove_table_column_assignment_template = (
        RemoveTableColumnAssignmentTemplate.Field()
    )
