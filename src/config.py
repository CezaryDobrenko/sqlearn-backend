import os
import pathlib
from typing import Type


def get_db_uri(**kwargs):
    return "{drivername}://{username}:{password}@{host}:{port}/{database}".format(
        drivername=kwargs.get("drivername"),
        username=kwargs.get("username"),
        password=kwargs.get("password"),
        host=kwargs.get("host"),
        port=kwargs.get("port"),
        database=kwargs.get("database"),
    )


BASE_PATH = pathlib.Path(__file__).parent


class BaseConfig:
    DEBUG = False

    DATABASE = {
        "drivername": "postgresql",
        "username": "postgres",
        "password": "password",
        "host": "localhost",
        "port": "5432",
        "database": "postgres",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(**DATABASE)


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True

    DATABASE = {
        "drivername": "postgresql",
        "username": "postgres",
        "password": "password",
        "host": "localhost",
        "port": "5432",
        "database": "testdb",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(**DATABASE)


class LocalConfig(BaseConfig):
    DEBUG = True

    DATABASE = {
        "drivername": "postgresql",
        "username": "postgres",
        "password": "password",
        "host": "localhost",
        "port": "8080",
        "database": "postgres",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(**DATABASE)


app_settings: str = os.environ.get("APP_SETTINGS", "DevConfig")

Config: Type[BaseConfig]
if app_settings == "DevConfig":
    Config = DevConfig
elif app_settings == "TestConfig":
    Config = TestConfig
elif app_settings == "LocalConfig":
    Config = LocalConfig
else:
    raise Exception("Invalid Config")

SALT: bytes = b"$2b$12$As5AULS67xcEs6kxZGQnhe"