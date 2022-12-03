from exceptions import AlreadyExists, ColumnException
from instance_access import authorize_access
from models.utils import transaction_scope
from modules.database_preset.application.managers.table_column_manager import (
    TableColumnManager,
)
from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.table import Table


class TableColumnManagementService:
    def __init__(self, session):
        self.session = session
        self.column_manager = TableColumnManager(session)

    @authorize_access(Table)
    def create(self, table_id: int, name: str, type: str, **kwargs) -> TableColumn:
        with transaction_scope(self.session) as session:
            table = session.query(Table).get(table_id)
            if not self.column_manager.can_create(table, name):
                raise AlreadyExists("Column with that name is already defined!")

            table_column = TableColumn(table_id=table_id, name=name, type=type)
            table_column.update(**kwargs)
            session.add(table_column)
        return table_column

    @authorize_access(TableColumn)
    def update(self, table_column_id: int, **kwargs) -> TableColumn:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumn).get(table_column_id)

            if not self.column_manager.can_update(table_column, **kwargs):
                raise ColumnException(action="update")

            table_column.update(**kwargs)
        return table_column

    @authorize_access(TableColumn)
    def remove(self, table_column_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumn).get(table_column_id)

            if not self.column_manager.can_delete(table_column):
                raise ColumnException(action="delete")

            session.delete(table_column)
        return True
