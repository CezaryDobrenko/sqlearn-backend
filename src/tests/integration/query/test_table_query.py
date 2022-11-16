from tests.utils import authenticated_request, gid


def test_authorized_node_table_query(
    db_session, graphql_client, user_factory, table_factory, database_factory
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(name="table", database=database)

    query = """
        query Table($id: ID!){
            authorizedNode(id: $id){
                ...on TableNode{
                    id
                    name
                }
            }
        }
    """
    variables = {"id": gid(table)}
    expected = {"authorizedNode": None}

    response = graphql_client.execute(
        query, variables=variables, context_value={"session": db_session, "request": {}}
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_tables_query(
    db_session, graphql_client, user_factory, database_factory, table_factory
):
    user = user_factory()
    database_1 = database_factory(name="database_1", user=user)
    table_1 = table_factory(name="table_1", database=database_1)
    table_2 = table_factory(name="table_2", database=database_1)
    database_2 = database_factory(name="database_2", user=user)
    table_3 = table_factory(name="table_3", database=database_2)
    other_user = user_factory()
    database_3 = database_factory(name="database_3", user=other_user)
    _ = table_factory(name="table_4", database=database_3)

    query = """
        query userTables{
            user{
                databases{
                    edges{
                        node{
                            name
                            tables{
                                edges{
                                    node{
                                        name
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
                            "name": database_1.name,
                            "tables": {
                                "edges": [
                                    {"node": {"name": table_1.name}},
                                    {"node": {"name": table_2.name}},
                                ]
                            },
                        }
                    },
                    {
                        "node": {
                            "name": database_2.name,
                            "tables": {"edges": [{"node": {"name": table_3.name}}]},
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
