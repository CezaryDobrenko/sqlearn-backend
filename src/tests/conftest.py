from typing import Optional
from unittest.mock import MagicMock

import pytest
from graphene.test import Client
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug import Request

from api.graphql_api import schema
from config import TestConfig
from models.base_model import AbstractModel
from tests.factories import UserFactory

register(UserFactory)


class RequestFactory:
    def __call__(
        self,
        method: str = "GET",
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
    ) -> Request:
        request = MagicMock(spec=Request)
        request.method = method
        request.headers = headers if headers else {}
        request.cookies = cookies if cookies else {}
        return request


@pytest.fixture(scope="session")
def db_connection():
    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    AbstractModel.metadata.drop_all(engine)
    AbstractModel.metadata.create_all(engine)
    connection = engine.connect()
    AbstractModel.metadata.bind = engine

    yield connection

    AbstractModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(db_connection):
    transaction = db_connection.begin()
    session = sessionmaker(bind=db_connection)
    db_session = session()

    factories = [UserFactory]
    for factory in factories:
        factory._meta.sqlalchemy_session = db_session

    yield db_session

    transaction.rollback()
    db_session.close()


@pytest.fixture
def graphql_client():
    return Client(schema)


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def cookie_session():
    return {}
