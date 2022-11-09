from jwt_token import TokenType
from models import User


def test_sign_up_mutation(db_session, graphql_client, jwt_service, cookie_session):
    email = "test@gmail.com"
    password = "secretpassword"

    query = """
        mutation signUp($email: String!, $password: String!){
            signUp(email: $email, password: $password){
                accessToken
            }
        }
    """
    variables = {"email": email, "password": password}
    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "cookie_session": cookie_session},
    )

    access_token = response["data"]["signUp"]["accessToken"]
    access_payload = jwt_service.get_token_payload(
        access_token, TokenType.AUTHORIZATION.value
    )
    user = db_session.query(User).first()
    assert not response.get("errors")
    assert access_payload["user_id"] == user.id
    assert access_payload["token_type"] == TokenType.AUTHORIZATION.value
    assert "set_cookie" in cookie_session
    assert "refresh_token" in cookie_session["set_cookie"]
    assert "Path=/" in cookie_session["set_cookie"]
    assert "HttpOnly" in cookie_session["set_cookie"]


def test_sign_in_mutation(
    db_session, graphql_client, jwt_service, cookie_session, user_factory
):
    email = "test@gmail.com"
    password = "secret@pAs$word997"
    user = user_factory(email=email)

    query = """
        mutation signIn($email: String!, $password: String!){
            signIn(email: $email, password: $password){
                accessToken
            }
        }
    """
    variables = {"email": email, "password": password}
    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "cookie_session": cookie_session},
    )

    access_token = response["data"]["signIn"]["accessToken"]
    access_payload = jwt_service.get_token_payload(
        access_token, TokenType.AUTHORIZATION.value
    )
    user = db_session.query(User).first()
    assert not response.get("errors")
    assert access_payload["user_id"] == user.id
    assert access_payload["token_type"] == TokenType.AUTHORIZATION.value
    assert "set_cookie" in cookie_session
    assert "refresh_token" in cookie_session["set_cookie"]
    assert "Path=/" in cookie_session["set_cookie"]
    assert "HttpOnly" in cookie_session["set_cookie"]


def test_refresh_token_mutation(
    db_session, graphql_client, request_factory, jwt_service, user_factory
):
    user = user_factory(email="test@gmail.com")
    refresh_token = jwt_service.create_refresh_token(user.id)
    request = request_factory(cookies={"refresh_token": refresh_token})

    query = """
        mutation refreshToken{
            refreshToken{
                accessToken
            }
        }
    """
    response = graphql_client.execute(
        query,
        context_value={"session": db_session, "request": request},
    )

    access_token = response["data"]["refreshToken"]["accessToken"]
    access_payload = jwt_service.get_token_payload(
        access_token, TokenType.AUTHORIZATION.value
    )
    assert not response.get("errors")
    assert access_payload["user_id"] == user.id
    assert access_payload["token_type"] == TokenType.AUTHORIZATION.value
