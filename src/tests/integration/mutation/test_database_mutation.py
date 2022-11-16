from modules.database_preset.domain.models.database import Database
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
