from graphene import ID, Boolean, Field, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.database import DatabaseAssignmentTemplateNode, DatabaseNode
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.database_template_service import (
    DatabaseAssignmentTemplateManagementService,
)
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


class CreateDatabaseAssignmentTemplate(Mutation):
    database = Field(DatabaseAssignmentTemplateNode)

    class Arguments:
        assignment_template_id = ID(required=True)
        name = String(required=True)

    @authentication_required()
    def mutate(self, info, assignment_template_id: str, name: str, **kwargs):
        session = info.context["session"]
        assignment_template_pk = retrieve_id(assignment_template_id)
        manager = DatabaseAssignmentTemplateManagementService(session)
        database = manager.create(assignment_template_pk, name, **kwargs)
        return CreateDatabaseAssignmentTemplate(database=database)


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


class UpdateDatabaseAssignmentTemplate(Mutation):
    database = Field(DatabaseAssignmentTemplateNode)

    class Arguments:
        database_assignment_template_id = ID(required=True)
        name = String()

    @authentication_required()
    def mutate(self, info, database_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        database_assignment_template_pk = retrieve_id(database_assignment_template_id)
        manager = DatabaseAssignmentTemplateManagementService(session)
        database = manager.update(database_assignment_template_pk, **kwargs)
        return UpdateDatabaseAssignmentTemplate(database=database)


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


class RemoveDatabaseAssignmentTemplate(Mutation):
    is_removed = Boolean()

    class Arguments:
        database_assignment_template_id = ID(required=True)

    @authentication_required()
    def mutate(self, info, database_assignment_template_id: str, **kwargs):
        session = info.context["session"]
        database_assignment_template_pk = retrieve_id(database_assignment_template_id)
        manager = DatabaseAssignmentTemplateManagementService(session)
        is_removed = manager.remove(database_assignment_template_pk, **kwargs)
        return RemoveDatabaseAssignmentTemplate(is_removed=is_removed)


class DatabaseMutation(ObjectType):
    create_database = CreateDatabase.Field()
    update_database = UpdateDatabase.Field()
    remove_database = RemoveDatabase.Field()

    create_database_assignment_template = CreateDatabaseAssignmentTemplate.Field()
    update_database_assignment_template = UpdateDatabaseAssignmentTemplate.Field()
    remove_database_assignment_template = RemoveDatabaseAssignmentTemplate.Field()
