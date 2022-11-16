from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.database import DatabaseNode
from api.graphql_api.utils import retrieve_id
from modules.database_preset.application.services.database_service import (
    DatabaseManagementService,
)


class CreateDatabase(Mutation):
    database = Field(DatabaseNode)

    class Arguments:
        name = String(required=True)

    @authentication_required()
    def mutate(self, info, name: str, **kwargs):
        session = info.context["session"]
        manager = DatabaseManagementService(session)
        database = manager.create(name, **kwargs)
        return CreateDatabase(database=database)


class UpdateDatabase(Mutation):
    database = Field(DatabaseNode)

    class Arguments:
        database_id = ID(required=True)
        name = String()

    @authentication_required()
    def mutate(self, info, database_id: str, **kwargs):
        session = info.context["session"]
        database_pk = retrieve_id(database_id)
        manager = DatabaseManagementService(session)
        database = manager.update(database_pk, **kwargs)
        return UpdateDatabase(database=database)


class RemoveDatabase(Mutation):
    is_removed = Boolean()

    class Arguments:
        database_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, database_id: str, **kwargs):
        session = info.context["session"]
        database_pk = retrieve_id(database_id)
        manager = DatabaseManagementService(session)
        is_removed = manager.remove(database_pk, **kwargs)
        return RemoveDatabase(is_removed=is_removed)


class DatabaseMutation(ObjectType):
    create_database = CreateDatabase.Field()
    update_database = UpdateDatabase.Field()
    remove_database = RemoveDatabase.Field()
