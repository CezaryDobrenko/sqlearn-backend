from tests.builders import (
    build_assignment_template_database,
    build_assignment_template_database_variant_2,
)
from tests.utils import authenticated_request, gid


def test_create_table_row_assignment_template_with_id_mutation(
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
    row_data = [["id", "5"], ["name", "Example"], ["user_id", "1"]]

    query = """
        mutation createTableAssignmentRow($tableAssignmentTemplateId: ID!, $rowData: [[String]]){
            createTableAssignmentRow(tableAssignmentTemplateId: $tableAssignmentTemplateId, rowData: $rowData){
                row{
                    ordinal
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
                "ordinal": 3,
                "cells": {
                    "edges": [
                        {"node": {"value": "5"}},
                        {"node": {"value": "Example"}},
                        {"node": {"value": "1"}},
                    ]
                },
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
    assert table.autoincrement_index == 6


def test_create_table_row_assignment_template_without_id_mutation(
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
    row_data = [["name", "Example"], ["user_id", "1"]]

    query = """
        mutation createTableAssignmentRow($tableAssignmentTemplateId: ID!, $rowData: [[String]]){
            createTableAssignmentRow(tableAssignmentTemplateId: $tableAssignmentTemplateId, rowData: $rowData){
                row{
                    ordinal
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
                "ordinal": 3,
                "cells": {
                    "edges": [
                        {"node": {"value": "3"}},
                        {"node": {"value": "Example"}},
                        {"node": {"value": "1"}},
                    ]
                },
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
    assert table.autoincrement_index == 4


def test_remove_table_row_assignment_template_mutation(
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
    database_template = build_assignment_template_database_variant_2(
        assignment_template
    )
    (
        user_table,
        paintings_table,
        exibition_table,
        warehouse_table,
        test_table,
    ) = database_template.tables.all()
    row, _ = user_table.rows.all()

    query = """
        mutation removeTableAssignmentRow($tableRowAssignmentTemplateId: ID!){
            removeTableAssignmentRow(tableRowAssignmentTemplateId: $tableRowAssignmentTemplateId){
                isRemoved
            }
        }
    """
    variables = {"tableRowAssignmentTemplateId": gid(row)}
    expected = {"removeTableAssignmentRow": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    _, _, paintings_user_id_col = paintings_table.columns.all()
    _, _, warehouse_user_id_col = warehouse_table.columns.all()
    _, test_user_id_col = test_table.columns.all()
    user_id_col, _ = user_table.columns.all()
    assert not response.get("errors")
    assert response["data"] == expected
    assert user_table.rows.count() == 1
    assert paintings_table.rows.count() == 1
    assert exibition_table.rows.count() == 1
    assert warehouse_table.rows.count() == 1
    assert [cell.value for cell in user_id_col.data] == ["2"]
    assert [cell.value for cell in paintings_user_id_col.data] == ["2"]
    assert [cell.value for cell in warehouse_user_id_col.data] == ["2"]
    assert [cell.value for cell in test_user_id_col.data] == ["2"]


def test_update_table_row_assignment_template_mutation(
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
    database_template = build_assignment_template_database_variant_2(
        assignment_template
    )
    (
        user_table,
        paintings_table,
        _,
        warehouse_table,
        test_table,
    ) = database_template.tables.all()
    first_user_row, _ = user_table.rows.all()
    new_id = "5"
    new_name = "Example"
    new_values = [["id", new_id], ["name", new_name]]

    query = """
        mutation updateTableAssignmentRow($tableRowAssignmentTemplateId: ID!, $rowData: [[String]]){
            updateTableAssignmentRow(tableRowAssignmentTemplateId: $tableRowAssignmentTemplateId, rowData: $rowData){
                row{
                    id
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
    variables = {
        "tableRowAssignmentTemplateId": gid(first_user_row),
        "rowData": new_values,
    }
    expected = {
        "updateTableAssignmentRow": {
            "row": {
                "id": gid(first_user_row),
                "cells": {
                    "edges": [
                        {"node": {"value": new_id}},
                        {"node": {"value": new_name}},
                    ]
                },
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    _, _, paintings_user_id_col = paintings_table.columns.all()
    _, _, warehouse_user_id_col = warehouse_table.columns.all()
    _, test_user_id_col = test_table.columns.all()
    user_id_col, _ = user_table.columns.all()
    assert not response.get("errors")
    assert response["data"] == expected
    assert [cell.value for cell in user_id_col.data] == ["5", "2"]
    assert [cell.value for cell in paintings_user_id_col.data] == ["5", "2"]
    assert [cell.value for cell in warehouse_user_id_col.data] == ["5", "2"]
    assert [cell.value for cell in test_user_id_col.data] == ["5", "2"]


def test_update_table_cell_assignment_template_mutation(
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
    database_template = build_assignment_template_database_variant_2(
        assignment_template
    )
    (
        user_table,
        paintings_table,
        exibition_table,
        warehouse_table,
        test_table,
    ) = database_template.tables.all()
    user_id_col, _ = user_table.columns.all()
    cell, _ = user_id_col.data.all()
    new_value = "5"

    query = """
        mutation updateTableAssignmentCell($tableColumnDataTemplateId: ID!, $value: String){
            updateTableAssignmentCell(tableColumnDataTemplateId: $tableColumnDataTemplateId, value: $value){
                cell{
                    value
                }
            }
        }
    """
    variables = {"tableColumnDataTemplateId": gid(cell), "value": new_value}
    expected = {"updateTableAssignmentCell": {"cell": {"value": "5"}}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    _, _, paintings_user_id_col = paintings_table.columns.all()
    _, _, warehouse_user_id_col = warehouse_table.columns.all()
    _, test_user_id_col = test_table.columns.all()
    user_id_col, _ = user_table.columns.all()
    assert not response.get("errors")
    assert response["data"] == expected
    assert user_table.rows.count() == 2
    assert user_table.autoincrement_index == 6
    assert paintings_table.rows.count() == 2
    assert warehouse_table.rows.count() == 2
    assert exibition_table.rows.count() == 2
    assert [cell.value for cell in user_id_col.data] == ["5", "2"]
    assert [cell.value for cell in paintings_user_id_col.data] == ["5", "2"]
    assert [cell.value for cell in warehouse_user_id_col.data] == ["5", "2"]
    assert [cell.value for cell in test_user_id_col.data] == ["5", "2"]
