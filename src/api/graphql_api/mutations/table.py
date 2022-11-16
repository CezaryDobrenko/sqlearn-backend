from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.table import TableNode
from api.graphql_api.utils import retrieve_id
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


class TableMutation(ObjectType):
    create_table = CreateTable.Field()
    update_table = UpdateTable.Field()
    remove_table = RemoveTable.Field()
