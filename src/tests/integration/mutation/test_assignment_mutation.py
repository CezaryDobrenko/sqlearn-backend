from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.database import DatabaseAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from tests.builders import build_assignment_template_database, build_preset_database
from tests.utils import authenticated_request, gid


def test_create_assignment_template_when_first_assignment_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    title = "new_assignment"
    description = "new_description"
    owner_solution = "SELECT * FROM users"

    query = """
        mutation createAssignmentTemplate(
            $quizTemplateId: ID!,
            $title: String!,
            $description: String,
            $ownerSolution: String
        ){
            createAssignmentTemplate(
                quizTemplateId: $quizTemplateId,
                title: $title,
                description: $description,
                ownerSolution: $ownerSolution
            ){
                assignmentTemplate{
                    title
                    description
                    ownerSolution
                }
            }
        }
    """
    variables = {
        "quizTemplateId": gid(quiz_template),
        "title": title,
        "description": description,
        "ownerSolution": owner_solution,
    }
    expected = {
        "createAssignmentTemplate": {
            "assignmentTemplate": {
                "title": title,
                "description": description,
                "ownerSolution": owner_solution,
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assignment_templates = db_session.query(AssignmentTemplate)
    assignment_databases = db_session.query(DatabaseAssignmentTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert assignment_templates.count() == 1
    assert assignment_databases.count() == 1


def test_create_assignment_template_when_next_assignment_mutation(
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
    assignment_template = assignment_template_factory(
        quiz_template=quiz_template, ordinal=1
    )
    build_assignment_template_database(assignment_template)
    title = "next_assigment_title"
    description = "next_assigment_description"
    owner_solution = "next_assigment_owner_solution"

    query = """
        mutation createAssignmentTemplate(
            $quizTemplateId: ID!,
            $title: String!,
            $description: String,
            $ownerSolution: String
        ){
            createAssignmentTemplate(
                quizTemplateId: $quizTemplateId,
                title: $title,
                description: $description,
                ownerSolution: $ownerSolution
            ){
                assignmentTemplate{
                    title
                    description
                    ownerSolution
                }
            }
        }
    """
    variables = {
        "quizTemplateId": gid(quiz_template),
        "title": title,
        "description": description,
        "ownerSolution": owner_solution,
    }
    expected = {
        "createAssignmentTemplate": {
            "assignmentTemplate": {
                "title": title,
                "description": description,
                "ownerSolution": owner_solution,
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assignment_templates = db_session.query(AssignmentTemplate)
    database_templates = db_session.query(DatabaseAssignmentTemplate)
    table_templates = db_session.query(TableAssignmentTemplate)
    column_templates = db_session.query(TableColumnAssignmentTemplate)
    relation_templates = db_session.query(TableRelationAssignmentTemplate)
    data_templates = db_session.query(TableColumnDataTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert assignment_templates.count() == 1 * 2
    assert database_templates.count() == 1 * 2
    assert table_templates.count() == 2 * 2
    assert column_templates.count() == 5 * 2
    assert data_templates.count() == 10 * 2
    assert relation_templates.count() == 1 * 2


def test_update_assignment_template_mutation(
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
    assignment_template = assignment_template_factory(
        quiz_template=quiz_template,
        ordinal=1,
        title="old_title",
        description="old_description",
        owner_solution="old_owner_solution",
    )
    build_assignment_template_database(assignment_template)
    new_title = "new_assigment_title"
    new_description = "next_assigment_description"
    new_owner_solution = "next_assigment_owner_solution"
    preset_database = build_preset_database(user)

    query = """
        mutation updateAssignmentTemplate(
            $assignmentTemplateId: ID!,
            $title: String,
            $databaseId: ID,
            $description: String,
            $ownerSolution: String
        ){
            updateAssignmentTemplate(
                assignmentTemplateId: $assignmentTemplateId,
                title: $title,
                databaseId: $databaseId,
                description: $description,
                ownerSolution: $ownerSolution
            ){
                assignmentTemplate{
                    title
                    description
                    ownerSolution
                }
            }
        }
    """
    variables = {
        "assignmentTemplateId": gid(assignment_template),
        "databaseId": gid(preset_database),
        "title": new_title,
        "description": new_description,
        "ownerSolution": new_owner_solution,
    }
    expected = {
        "updateAssignmentTemplate": {
            "assignmentTemplate": {
                "title": new_title,
                "description": new_description,
                "ownerSolution": new_owner_solution,
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    database_templates = db_session.query(DatabaseAssignmentTemplate)
    table_templates = db_session.query(TableAssignmentTemplate)
    column_templates = db_session.query(TableColumnAssignmentTemplate)
    relation_templates = db_session.query(TableRelationAssignmentTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert database_templates.count() == 1
    assert table_templates.count() == 3
    assert column_templates.count() == 8
    assert relation_templates.count() == 2


def test_remove_assignment_template_mutation(
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
    assignment_template = assignment_template_factory(
        quiz_template=quiz_template,
        ordinal=1,
        title="old_title",
        description="old_description",
        owner_solution="old_owner_solution",
    )
    build_assignment_template_database(assignment_template)

    query = """
        mutation removeAssignmentTemplate($assignmentTemplateId: ID!){
            removeAssignmentTemplate(assignmentTemplateId: $assignmentTemplateId,){
                isRemoved
            }
        }
    """
    variables = {"assignmentTemplateId": gid(assignment_template)}
    expected = {"removeAssignmentTemplate": {"isRemoved": True}}

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
    assert asignment_templates.count() == 0
    assert database_templates.count() == 0
    assert table_templates.count() == 0
    assert column_templates.count() == 0
    assert relation_templates.count() == 0
    assert data_templates.count() == 0


def test_remove_assignment_template_without_database_mutation(
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
    assignment_template = assignment_template_factory(
        quiz_template=quiz_template,
        ordinal=1,
        title="old_title",
        description="old_description",
        owner_solution="old_owner_solution",
    )

    query = """
        mutation removeAssignmentTemplate($assignmentTemplateId: ID!){
            removeAssignmentTemplate(assignmentTemplateId: $assignmentTemplateId,){
                isRemoved
            }
        }
    """
    variables = {"assignmentTemplateId": gid(assignment_template)}
    expected = {"removeAssignmentTemplate": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
