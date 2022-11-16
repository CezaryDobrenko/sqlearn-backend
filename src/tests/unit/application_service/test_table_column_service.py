import pytest

from exceptions import RelationException
from modules.database_preset.application.services.table_column_service import (
    TableColumnManagementService,
)


def test_update_table_column_when_relation_exists(
    user_factory,
    db_session,
    database_factory,
    table_factory,
    table_column_factory,
    table_relation_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(database=database, name="users")
    relation_table = table_factory(database=database, name="paining")
    column = table_column_factory(table=table, name="id")
    _ = table_column_factory(table=table, name="user_id")
    _ = table_relation_factory(
        name="user_paining_fk",
        relation_column_name="user_id",
        relation_table=relation_table,
        table_column_name="id",
        table=table,
    )

    service = TableColumnManagementService(db_session)

    with pytest.raises(RelationException):
        update = {"current_user": user, "name": "other_id"}
        service.update(column.id, is_relationship=True, **update)


def test_remove_table_column_when_relation_exists(
    user_factory,
    db_session,
    database_factory,
    table_factory,
    table_column_factory,
    table_relation_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(database=database, name="users")
    relation_table = table_factory(database=database, name="paining")
    column = table_column_factory(table=table, name="id")
    _ = table_column_factory(table=table, name="user_id")
    _ = table_relation_factory(
        name="user_paining_fk",
        relation_column_name="user_id",
        relation_table=relation_table,
        table_column_name="id",
        table=table,
    )

    service = TableColumnManagementService(db_session)

    with pytest.raises(RelationException):
        service.remove(column.id, **{"current_user": user})
