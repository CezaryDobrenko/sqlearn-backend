# SQLearn-Backend
## version: 1.0.0
Backend API description

## Tech

List of technologies used in the SQLearn-Backend project:

- [Python 3.10] - application created using python language.
- [Flask] - web framework.
- [GraphQL] - query language API.
- [SQLAlchemy] - SQL toolkit and ORM.
- [Alembic] - database migration tool.
- [Pytest] - test framework.
- [Fixtures] - database data loader.
- [Docker] - great UI boilerplate for modern web apps.
- [Black] - code formatter.
- [Isort] - sort imports library.
- [Flake8] - lint wrapper.

## Installation

It is recommended to use docker when installing software

```sh
docker-compose up
```

## Development

Run linters
```sh
make lint
```

Run project tests and coverate report
```sh
make test
make test-cov
```

Reload data and database
```sh
make reload-db
make reload-data
```

Run and create migrations
```sh
make migration
make name=new_migration create-migration
```

[//]: # (links)
   [Python 3.10]: <https://www.python.org/downloads/release/python-3100/>
   [Flask]: <https://flask.palletsprojects.com/en/2.2.x/>
   [GraphQL]: <https://graphene-python.org/>
   [SQLAlchemy]: <https://www.sqlalchemy.org/>
   [Alembic]: <https://alembic.sqlalchemy.org/en/latest/>
   [Pytest]: <https://docs.pytest.org/en/7.2.x/>
   [Fixtures]: <https://py-yaml-fixtures.readthedocs.io/en/latest/>
   [Docker]: <https://docs.docker.com/>
   [Black]: <https://pypi.org/project/black/>
   [Isort]: <https://isort.readthedocs.io/en/latest/>
   [Flake8]: <https://flake8.pycqa.org/en/latest/>
