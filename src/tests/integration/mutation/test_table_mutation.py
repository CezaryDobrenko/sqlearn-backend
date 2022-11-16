from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table
from tests.utils import authenticated_request, gid


def test_create_database_mutation(
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
