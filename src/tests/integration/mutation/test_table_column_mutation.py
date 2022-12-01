from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.database_preset.domain.models.column import ColumnType, TableColumn
from tests.builders import build_assignment_template_database
from tests.utils import authenticated_request, gid


def test_create_table_column_mutation(
    db_session, graphql_client, user_factory, database_factory, table_factory
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(database=database)
    name = "column_name"
    type = "TEXT"
    length = 300
    is_null = False
    is_unique = True

    query = """
        mutation createTableColumn(
            $tableId: ID!,
            $name: String!,
            $type: String!,
            $length: Int,
            $isNull: Boolean,
            $isUnique: Boolean
        ){
            createTableColumn(
                tableId: $tableId,
                name: $name,
                type: $type,
                length: $length,
                isNull: $isNull,
                isUnique: $isUnique
            ){
                column{
                    name
                    type
                    length
                    isNull
                    isUnique
                    table{
                        id
                    }
                }
            }
        }
    """
    variables = {
        "tableId": gid(table),
        "name": name,
        "type": type,
        "length": length,
        "isNull": is_null,
        "isUnique": is_unique,
    }
    expected = {
        "createTableColumn": {
            "column": {
                "name": name,
                "type": type,
                "length": length,
                "isNull": is_null,
                "isUnique": is_unique,
                "table": {"id": gid(table)},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    columns = db_session.query(TableColumn)
    assert not response.get("errors")
    assert response["data"] == expected
    assert columns.count() == 1


def test_update_table_column_mutation(
    db_session,
    graphql_client,
    user_factory,
    database_factory,
    table_factory,
    table_column_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(database=database)
    column = table_column_factory(
        table=table,
        name="old_name",
        type="TEXT",
        length=200,
        is_null=True,
        is_unique=True,
    )
    new_name = "new_name"
    new_type = "INTEGER"
    new_length = 15
    new_is_null = False
    new_is_unique = False

    query = """
        mutation updateTableColumn(
            $tableColumnId: ID!,
            $name: String,
            $type: String,
            $length: Int,
            $isNull: Boolean,
            $isUnique: Boolean
        ){
            updateTableColumn(
                tableColumnId: $tableColumnId,
                name: $name,
                type: $type,
                length: $length,
                isNull: $isNull,
                isUnique: $isUnique
            ){
                column{
                    name
                    type
                    length
                    isNull
                    isUnique
                    table{
                        id
                    }
                }
            }
        }
    """
    variables = {
        "tableColumnId": gid(column),
        "name": new_name,
        "type": new_type,
        "length": new_length,
        "isNull": new_is_null,
        "isUnique": new_is_unique,
    }
    expected = {
        "updateTableColumn": {
            "column": {
                "name": new_name,
                "type": new_type,
                "length": new_length,
                "isNull": new_is_null,
                "isUnique": new_is_unique,
                "table": {"id": gid(table)},
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
    assert column.name == new_name
    assert column.type == ColumnType.INTEGER
    assert column.length == new_length
    assert column.is_null == new_is_null


def test_remove_table_column_mutation(
    db_session,
    graphql_client,
    user_factory,
    database_factory,
    table_factory,
    table_column_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(database=database, name="users")
    column = table_column_factory(table=table)

    query = """
        mutation removeTableColumn($tableColumnId: ID!){
            removeTableColumn(tableColumnId: $tableColumnId){
                isRemoved
            }
        }
    """
    variables = {"tableColumnId": gid(column)}
    expected = {"removeTableColumn": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    columns = db_session.query(TableColumn)
    assert not response.get("errors")
    assert response["data"] == expected
    assert columns.count() == 0


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
    name = "column_name"
    type = "TEXT"
    length = 300
    is_null = False
    is_unique = True

    query = """
        mutation createTableColumnAssignmentTemplate(
            $tableAssignmentTemplateId: ID!,
            $name: String!,
            $type: String!,
            $length: Int,
            $isNull: Boolean,
            $isUnique: Boolean
        ){
            createTableColumnAssignmentTemplate(
                tableAssignmentTemplateId: $tableAssignmentTemplateId,
                name: $name,
                type: $type,
                length: $length,
                isNull: $isNull,
                isUnique: $isUnique
            ){
                column{
                    name
                    type
                    length
                    isNull
                    isUnique
                    tableAssignmentTemplate{
                        id
                    }
                }
            }
        }
    """
    variables = {
        "tableAssignmentTemplateId": gid(table),
        "name": name,
        "type": type,
        "length": length,
        "isNull": is_null,
        "isUnique": is_unique,
    }
    expected = {
        "createTableColumnAssignmentTemplate": {
            "column": {
                "name": name,
                "type": type,
                "length": length,
                "isNull": is_null,
                "isUnique": is_unique,
                "tableAssignmentTemplate": {"id": gid(table)},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    columns = db_session.query(TableColumnAssignmentTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert columns.count() == 6


def test_update_table_column_assignment_template_without_relation_mutation(
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
    _, column, _ = table.columns.all()
    new_name = "new_name"
    new_type = "INTEGER"
    new_length = 15
    new_is_null = False
    new_is_unique = False

    query = """
        mutation updateTableColumnAssignmentTemplate(
            $columnAssignmentTemplateId: ID!,
            $name: String,
            $type: String,
            $length: Int,
            $isNull: Boolean,
            $isUnique: Boolean
        ){
            updateTableColumnAssignmentTemplate(
                columnAssignmentTemplateId: $columnAssignmentTemplateId,
                name: $name,
                type: $type,
                length: $length,
                isNull: $isNull,
                isUnique: $isUnique
            ){
                column{
                    name
                    type
                    length
                    isNull
                    isUnique
                    tableAssignmentTemplate{
                        id
                    }
                }
            }
        }
    """
    variables = {
        "columnAssignmentTemplateId": gid(column),
        "name": new_name,
        "type": new_type,
        "length": new_length,
        "isNull": new_is_null,
        "isUnique": new_is_unique,
    }
    expected = {
        "updateTableColumnAssignmentTemplate": {
            "column": {
                "name": new_name,
                "type": new_type,
                "length": new_length,
                "isNull": new_is_null,
                "isUnique": new_is_unique,
                "tableAssignmentTemplate": {"id": gid(table)},
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
    assert column.name == new_name
    assert column.type == ColumnType.INTEGER
    assert column.length == new_length
    assert column.is_null == new_is_null


def test_remove_table_column_assignment_template_without_relation_mutation(
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
    _, column, _ = table.columns.all()

    query = """
        mutation removeTableColumnAssignmentTemplate($columnAssignmentTemplateId: ID!){
            removeTableColumnAssignmentTemplate(columnAssignmentTemplateId: $columnAssignmentTemplateId){
                isRemoved
            }
        }
    """
    variables = {"columnAssignmentTemplateId": gid(column)}
    expected = {"removeTableColumnAssignmentTemplate": {"isRemoved": True}}

    data = db_session.query(TableColumnDataTemplate)

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    columns = db_session.query(TableColumnAssignmentTemplate)
    data = db_session.query(TableColumnDataTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert columns.count() == 4
    assert data.count() == 8
