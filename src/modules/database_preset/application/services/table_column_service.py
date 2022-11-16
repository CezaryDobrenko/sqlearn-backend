from exceptions import RelationException
from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
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
    def create(self, table_id: int, name: str, **kwargs) -> TableColumn:
        with transaction_scope(self.session) as session:
            table_column, is_created = get_or_create(
                session,
                TableColumn,
                table_id=table_id,
                name=name,
            )
            if is_created:
                table_column.update(**kwargs)
        return table_column

    @authorize_access(TableColumn)
    def update(
        self, table_column_id: int, is_relationship: bool, **kwargs
    ) -> TableColumn:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumn).get(table_column_id)
            relations = self.column_manager.get_relations(table_column)

            if relations.first() and is_relationship:
                raise RelationException(action="update")

            table_column.update(**kwargs)
        return table_column

    @authorize_access(TableColumn)
    def remove(self, table_column_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumn).get(table_column_id)
            relations = self.column_manager.get_relations(table_column)

            if relations.first():
                raise RelationException(action="delete")

            session.delete(table_column)
        return True
