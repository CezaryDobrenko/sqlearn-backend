from tests.utils import authenticated_request, gid


def test_authorized_node_database_query(
    db_session, graphql_client, user_factory, database_factory
):
    user = user_factory()
    database = database_factory(name="database", user=user)

    query = """
        query Database($id: ID!){
            authorizedNode(id: $id){
                ...on DatabaseNode{
                    id
                    name
                }
            }
        }
    """
    variables = {"id": gid(database)}
    expected = {"authorizedNode": None}

    response = graphql_client.execute(
        query, variables=variables, context_value={"session": db_session, "request": {}}
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_databases_query(
    db_session, graphql_client, user_factory, database_factory
):
    user = user_factory()
    database_1 = database_factory(name="database_1", user=None)
    database_2 = database_factory(name="database_2", user=user)
    database_3 = database_factory(name="database_3", user=user)
    other_user = user_factory()
    _ = database_factory(name="database_4", user=other_user)

    query = """
        query userDatabases{
            user{
                databases{
                    edges{
                        node{
                            name
                        }
                    }
                }
            }
        }
    """
    expected = {
        "user": {
            "databases": {
                "edges": [
                    {
                        "node": {
                            "name": database_1.name,
                        }
                    },
                    {
                        "node": {
                            "name": database_2.name,
                        }
                    },
                    {
                        "node": {
                            "name": database_3.name,
                        }
                    },
                ]
            }
        }
    }

    response = graphql_client.execute(
        query,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_databases_relations_query(
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
    paintings_table = table_factory(database=database, name="paintings")
    _ = table_column_factory(table=paintings_table, name="id")
    _ = table_column_factory(table=paintings_table, name="name")
    _ = table_column_factory(table=paintings_table, name="user_id")
    cars_table = table_factory(database=database, name="cars")
    _ = table_column_factory(table=cars_table, name="id")
    _ = table_column_factory(table=cars_table, name="name")
    _ = table_column_factory(table=cars_table, name="user_id")
    _ = table_column_factory(table=cars_table, name="painting_id")

    relation = table_relation_factory(
        name="old_fk",
        action="SET_NULL",
        table=users_table,
        table_column_name="id",
        relation_table=paintings_table,
        relation_column_name="user_id",
    )

    query = """
        query DatabaseRelations{
            user{
                databases{
                    edges{
                        node{
                            name
                            relations{
                                edges{
                                    node{
                                        relationColumnName
                                        relationTable{
                                            name
                                        }
                                        tableColumnName
                                        table{
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """
    expected = {
        "user": {
            "databases": {
                "edges": [
                    {
                        "node": {
                            "name": database.name,
                            "relations": {
                                "edges": [
                                    {
                                        "node": {
                                            "relationColumnName": relation.relation_column_name,
                                            "relationTable": {
                                                "name": relation.relation_table.name
                                            },
                                            "tableColumnName": relation.table_column_name,
                                            "table": {"name": relation.table.name},
                                        }
                                    }
                                ]
                            },
                        }
                    }
                ]
            }
        }
    }

    response = graphql_client.execute(
        query,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
