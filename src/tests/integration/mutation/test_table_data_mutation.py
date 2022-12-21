from tests.builders import build_assignment_template_database
from tests.utils import authenticated_request, gid


def test_create_table_column_assignment_template_mutation(
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
    _, table = database_template.tables.all()
    row_data = [["id", "3"], ["name", "Example"], ["user_id", "1"]]

    query = """
        mutation createTableAssignmentRow($tableAssignmentTemplateId: ID!, $rowData: [[String]]){
            createTableAssignmentRow(tableAssignmentTemplateId: $tableAssignmentTemplateId, rowData: $rowData){
                row{
                    cells{
                        edges{
                            node{
                                value
                            }
                        }
                    }
                }
            }
        }
    """
    variables = {"tableAssignmentTemplateId": gid(table), "rowData": row_data}
    expected = {
        "createTableAssignmentRow": {
            "row": {
                "cells": {
                    "edges": [
                        {"node": {"value": "3"}},
                        {"node": {"value": "Example"}},
                        {"node": {"value": "1"}},
                    ]
                }
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
    # assert False
