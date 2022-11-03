import os

from sqlalchemy.orm import sessionmaker

from models.base_model import engine
from models.utils import transaction_scope

Session = sessionmaker(bind=engine)
session = Session()

print("---started---")

with transaction_scope(session):
    connection = engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute("DROP SCHEMA IF EXISTS public CASCADE;")
    cursor.execute("CREATE SCHEMA public;")
    connection.commit()
    cursor.close()
    connection.close()

    print("apply migrations")
    os.system("alembic upgrade head")

    print("load mocked data")
    os.system("python fixtures/load.py")

print("---finished---")

session.close()
