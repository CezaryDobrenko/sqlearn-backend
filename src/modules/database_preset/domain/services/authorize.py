from instance_access import has_user_access
from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.database import Database
from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table
from modules.user.domain.models.user import User


@has_user_access.register(Database)
def _has_user_access_database(instance: Database, user: User) -> bool:
    return instance.user == user


@has_user_access.register(Table)
def _has_user_access_table(instance: Table, user: User) -> bool:
    return instance.database.user == user


@has_user_access.register(TableColumn)
def _has_user_access_column(instance: TableColumn, user: User) -> bool:
    return instance.table.database.user == user


@has_user_access.register(TableRelation)
def _has_user_access_relation(instance: TableRelation, user: User) -> bool:
    return instance.table.database.user == user
