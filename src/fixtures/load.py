from py_yaml_fixtures import FixturesLoader
from py_yaml_fixtures.factories.sqlalchemy import SQLAlchemyModelFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import configure_mappers, sessionmaker

from config import Config
from models.base_model import AbstractModel


# list of our model classes to provide to the factory
def load_models():
    from models.user import User

    configure_mappers()

    return [User]


model_classes = load_models()

# database conntection config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# create the factory, and pass it to the fixtures loader
PY_YAML_FIXTURES_DIR = "fixtures"
factory = SQLAlchemyModelFactory(session, model_classes)
loader = FixturesLoader(factory, fixture_dirs=[PY_YAML_FIXTURES_DIR])

if __name__ == "__main__":
    AbstractModel.metadata.create_all(bind=engine)
    loader.create_all(
        lambda identifier, model, created: print(
            "{action} {identifier}: {model}".format(
                action="Creating" if created else "Updating",
                identifier=identifier.key,
                model=repr(model),
            )
        )
    )
