from tests.utils import authenticated_request, gid


def test_authorized_node_user_query(db_session, graphql_client, user_factory):
    user = user_factory()

    query = """
        query user($id: ID!){
            authorizedNode(id: $id){
                ...on UserNode{
                    id
                    email
                }
            }
        }
    """
    variables = {"id": gid(user)}
    expected = {"authorizedNode": None}

    response = graphql_client.execute(
        query, variables=variables, context_value={"session": db_session, "request": {}}
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_query(db_session, graphql_client, user_factory):
    user = user_factory()

    query = """
        query user{
            user{
                email
            }
        }
    """
    expected = {"user": {"email": user.email}}

    response = graphql_client.execute(
        query,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
