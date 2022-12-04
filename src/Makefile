test_config := TestConfig
local_config := LocalConfig
path := PYTHONPATH=.

test:
	$(path) APP_SETTINGS=$(test_config) pytest . -x

single-test:
	$(path) APP_SETTINGS=$(test_config) pytest $(test_path) -x

test-cov:
	$(path) APP_SETTINGS=$(test_config) pytest -x --cov=./ --cov-report=html

reload-db:
	$(path) APP_SETTINGS=$(local_config) python scripts/recreate_db.py

sql-in-memory:
	$(path) APP_SETTINGS=$(local_config) python scripts/test_db.py

reload-data:
	$(path) APP_SETTINGS=$(local_config) python fixtures/load.py

migration:
	$(path) APP_SETTINGS=$(local_config) alembic upgrade head

create-migration:
	$(path) APP_SETTINGS=$(local_config) alembic revision --autogenerate -m "$(name)"

create-db-diagram:
	$(path) APP_SETTINGS=$(local_config) python scripts/uml_diagram_generator.py

lint:
	black .
	isort .
	flake8 .