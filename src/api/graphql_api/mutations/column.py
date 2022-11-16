from graphene import ID, Boolean, Field, Int, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.table_column import TableColumnNode
from api.graphql_api.utils import retrieve_id
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

    @authentication_required()
    def mutate(self, info, table_id: str, name: str, **kwargs):
        session = info.context["session"]
        table_pk = retrieve_id(table_id)
        manager = TableColumnManagementService(session)
        column = manager.create(table_pk, name, **kwargs)
        return CreateTableColumn(column=column)


class UpdateTableColumn(Mutation):
    column = Field(TableColumnNode)

    class Arguments:
        table_column_id = ID(required=True)
        name = String()
        type = String()
        length = Int()
        is_null = Boolean()

    @authentication_required()
    def mutate(self, info, table_column_id: str, **kwargs):
        session = info.context["session"]
        table_column_pk = retrieve_id(table_column_id)
        is_relationship = True if "name" in kwargs or "type" in kwargs else False
        manager = TableColumnManagementService(session)
        column = manager.update(table_column_pk, is_relationship, **kwargs)
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


class TableColumnMutation(ObjectType):
    create_table_column = CreateTableColumn.Field()
    update_table_column = UpdateTableColumn.Field()
    remove_table_column = RemoveTableColumn.Field()
