import factory
from factory.alchemy import SQLAlchemyModelFactory

from models import User


class UserFactory(SQLAlchemyModelFactory):
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")
    password = factory.PostGenerationMethodCall("set_password", "secret@pAs$word997")

    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"
