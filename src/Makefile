test_config := TestConfig
local_config := LocalConfig
path := PYTHONPATH=.

test:
	$(path) APP_SETTINGS=$(test_config) pytest . -x

test-cov:
	$(path) APP_SETTINGS=$(test_config) pytest -x --cov=./ --cov-report=html

reload-db:
	$(path) APP_SETTINGS=$(local_config) python scripts/recreate_db.py

reload-data:
	$(path) APP_SETTINGS=$(local_config) python fixtures/load.py

migration:
	$(path) APP_SETTINGS=$(local_config) alembic upgrade head

create-migration:
	$(path) APP_SETTINGS=$(local_config) alembic revision --autogenerate -m "$(name)"

lint:
	black .
	isort .
	flake8 .