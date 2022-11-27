from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.database import DatabaseAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.database import Database
from tests.builders import build_assignment_template_database
from tests.utils import authenticated_request, gid


def test_create_database_mutation(db_session, graphql_client, user_factory):
    user = user_factory()
    name = "DML tutorial quiz"

    query = """
        mutation createDatabase($name: String!){
            createDatabase(name: $name){
                database{
                    name
                    user{
                        email
                    }
                }
            }
        }
    """
    variables = {"name": name}
    expected = {
        "createDatabase": {
            "database": {
                "name": name,
                "user": {"email": user.email},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    databases = db_session.query(Database)
    assert not response.get("errors")
    assert response["data"] == expected
    assert databases.count() == 1


def test_update_database_mutation(
    db_session, graphql_client, user_factory, database_factory
):
    user = user_factory()
    database = database_factory(user=user, name="old_name")
    new_name = "new_name"

    query = """
        mutation updateDatabase($databaseId: ID!, $name: String){
            updateDatabase(databaseId: $databaseId, name: $name){
                database{
                    name
                    user{
                        email
                    }
                }
            }
        }
    """
    variables = {"databaseId": gid(database), "name": new_name}
    expected = {
        "updateDatabase": {
            "database": {
                "name": new_name,
                "user": {"email": user.email},
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
    assert database.name == new_name


def test_remove_database_mutation(
    db_session, graphql_client, user_factory, database_factory
):
    user = user_factory()
    database = database_factory(user=user)

    query = """
        mutation removeDatabase($databaseId: ID!){
            removeDatabase(databaseId: $databaseId){
                isRemoved
            }
        }
    """
    variables = {"databaseId": gid(database)}
    expected = {"removeDatabase": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    databases = db_session.query(Database)
    assert not response.get("errors")
    assert response["data"] == expected
    assert databases.count() == 0


def test_create_database_assignment_template_mutation(
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
    name = "new_database_name"

    query = """
        mutation createDatabaseAssignmentTemplate($assignmentTemplateId: ID!, $name: String!){
            createDatabaseAssignmentTemplate(assignmentTemplateId: $assignmentTemplateId, name: $name){
                database{
                    name
                    assignmentTemplate{
                        title
                    }
                }
            }
        }
    """
    variables = {"assignmentTemplateId": gid(assignment_template), "name": name}
    expected = {
        "createDatabaseAssignmentTemplate": {
            "database": {
                "name": name,
                "assignmentTemplate": {"title": assignment_template.title},
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
    assert db_session.query(DatabaseAssignmentTemplate).count() == 1


def test_update_database_assignment_template_mutation(
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
    new_name = "new_database_name"

    query = """
        mutation updateDatabaseAssignmentTemplate($databaseAssignmentTemplateId: ID!, $name: String){
            updateDatabaseAssignmentTemplate(databaseAssignmentTemplateId: $databaseAssignmentTemplateId, name: $name){
                database{
                    name
                }
            }
        }
    """
    variables = {
        "databaseAssignmentTemplateId": gid(database_template),
        "name": new_name,
    }
    expected = {"updateDatabaseAssignmentTemplate": {"database": {"name": new_name}}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
    assert database_template.name == new_name


def test_remove_database_assignment_template_mutation(
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

    query = """
        mutation removeDatabaseAssignmentTemplate($databaseAssignmentTemplateId: ID!){
            removeDatabaseAssignmentTemplate(databaseAssignmentTemplateId: $databaseAssignmentTemplateId){
                isRemoved
            }
        }
    """
    variables = {"databaseAssignmentTemplateId": gid(database_template)}
    expected = {"removeDatabaseAssignmentTemplate": {"isRemoved": True}}

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
    assert database_templates.count() == 0
    assert table_templates.count() == 0
    assert column_templates.count() == 0
    assert relation_templates.count() == 0
    assert data_templates.count() == 0
