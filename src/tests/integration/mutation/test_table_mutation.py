from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.database import DatabaseAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.database import Database
from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table
from tests.builders import build_assignment_template_database, build_preset_database
from tests.utils import authenticated_request, gid


def test_create_table_mutation(
    db_session, graphql_client, user_factory, database_factory
):
    user = user_factory()
    database = database_factory(user=user)
    name = "table name"
    description = "description"

    query = """
        mutation createTable($databaseId: ID!, $name: String!, $description: String){
            createTable(databaseId: $databaseId, name: $name, description: $description){
                table{
                    name
                    description
                    database{
                        id
                    }
                }
            }
        }
    """
    variables = {"databaseId": gid(database), "name": name, "description": description}
    expected = {
        "createTable": {
            "table": {
                "name": name,
                "description": description,
                "database": {"id": gid(database)},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    tables = db_session.query(Table)
    assert not response.get("errors")
    assert response["data"] == expected
    assert tables.count() == 1


def test_update_table_mutation(
    db_session, graphql_client, user_factory, database_factory, table_factory
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(database=database, name="old_name", description="old_desc")
    new_name = "new_name"
    new_description = "new_description"

    query = """
        mutation updateTable($tableId: ID!, $name: String, $description: String){
            updateTable(tableId: $tableId, name: $name, description: $description){
                table{
                    name
                    description
                    database{
                        id
                    }
                }
            }
        }
    """
    variables = {
        "tableId": gid(table),
        "name": new_name,
        "description": new_description,
    }
    expected = {
        "updateTable": {
            "table": {
                "name": new_name,
                "description": new_description,
                "database": {"id": gid(database)},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
    assert table.name == new_name
    assert table.description == new_description


def test_remove_table_mutation(
    db_session,
    graphql_client,
    user_factory,
    database_factory,
    table_factory,
    table_column_factory,
    table_relation_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    users_table = table_factory(database=database, name="users")
    _ = table_column_factory(table=users_table, name="id")
    _ = table_column_factory(table=users_table, name="name")
    cars_table = table_factory(database=database, name="cars")
    _ = table_column_factory(table=cars_table, name="id")
    _ = table_column_factory(table=cars_table, name="name")
    _ = table_column_factory(table=cars_table, name="user_id")

    _ = table_relation_factory(
        name="old_fk",
        action="SET_NULL",
        table=users_table,
        table_column_name="id",
        relation_table=cars_table,
        relation_column_name="user_id",
    )

    query = """
        mutation removeTable($tableId: ID!){
            removeTable(tableId: $tableId){
                isRemoved
            }
        }
    """
    variables = {"tableId": gid(users_table)}
    expected = {"removeTable": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    tables = db_session.query(Table)
    relations = db_session.query(TableRelation)
    assert not response.get("errors")
    assert response["data"] == expected
    assert tables.count() == 1
    assert relations.count() == 0


def test_remove_table_with_relation_and_related_by_mutation(
    db_session, graphql_client, user_factory
):
    user = user_factory()
    preset_database = build_preset_database(user)
    _, table_to_delete, _ = preset_database.tables.all()

    query = """
        mutation removeTable($tableId: ID!){
            removeTable(tableId: $tableId){
                isRemoved
            }
        }
    """
    variables = {"tableId": gid(table_to_delete)}
    expected = {"removeTable": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    databases = db_session.query(Database)
    tables = db_session.query(Table)
    columns = db_session.query(TableColumn)
    relations = db_session.query(TableRelation)
    assert not response.get("errors")
    assert response["data"] == expected
    assert databases.count() == 1
    assert tables.count() == 2
    assert columns.count() == 5
    assert relations.count() == 0


def test_create_table_assignment_template_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    database_assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = database_assignment_template_factory(
        assignment_template=assignment_template
    )
    name = "new_table_name"
    description = "new_table_description"

    query = """
        mutation createTableAssignmentTemplate(
            $databaseAssignmentTemplateId: ID!,
            $name: String!,
            $description: String
        ){
            createTableAssignmentTemplate(
                databaseAssignmentTemplateId: $databaseAssignmentTemplateId,
                name: $name,
                description: $description
            ){
                table{
                    name
                    description
                    databaseAssignmentTemplate{
                        name
                    }
                }
            }
        }
    """
    variables = {
        "databaseAssignmentTemplateId": gid(database_template),
        "name": name,
        "description": description,
    }
    expected = {
        "createTableAssignmentTemplate": {
            "table": {
                "name": name,
                "description": description,
                "databaseAssignmentTemplate": {"name": database_template.name},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
    assert db_session.query(TableAssignmentTemplate).count() == 1


def test_update_table_assignment_template_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    database_assignment_template_factory,
    table_assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = database_assignment_template_factory(
        assignment_template=assignment_template
    )
    table_template = table_assignment_template_factory(
        database_assignment_template=database_template
    )
    new_name = "new_database_name"
    new_description = "new_database_description"

    query = """
        mutation updateTableAssignmentTemplate(
            $tableAssignmentTemplateId: ID!,
            $name: String,
            $description: String
        ){
            updateTableAssignmentTemplate(
                tableAssignmentTemplateId: $tableAssignmentTemplateId,
                name: $name, description:
                $description
            ){
                table{
                    name
                    description
                }
            }
        }
    """
    variables = {
        "tableAssignmentTemplateId": gid(table_template),
        "name": new_name,
        "description": new_description,
    }
    expected = {
        "updateTableAssignmentTemplate": {
            "table": {"name": new_name, "description": new_description}
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
    assert table_template.name == new_name
    assert table_template.description == new_description


def test_remove_table_assignment_template_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table_to_delete = database_template.tables.all()

    query = """
        mutation removeTableAssignmentTemplate($tableAssignmentTemplateId: ID!){
            removeTableAssignmentTemplate(tableAssignmentTemplateId: $tableAssignmentTemplateId){
                isRemoved
            }
        }
    """
    variables = {"tableAssignmentTemplateId": gid(table_to_delete)}
    expected = {"removeTableAssignmentTemplate": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    asignment_templates = db_session.query(AssignmentTemplate)
    database_templates = db_session.query(DatabaseAssignmentTemplate)
    table_templates = db_session.query(TableAssignmentTemplate)
    column_templates = db_session.query(TableColumnAssignmentTemplate)
    relation_templates = db_session.query(TableRelationAssignmentTemplate)
    data_templates = db_session.query(TableColumnDataTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert asignment_templates.count() == 1
    assert database_templates.count() == 1
    assert table_templates.count() == 1
    assert column_templates.count() == 2
    assert relation_templates.count() == 0
    assert data_templates.count() == 4
