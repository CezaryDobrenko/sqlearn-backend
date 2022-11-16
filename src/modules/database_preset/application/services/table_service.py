from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.database_preset.domain.models.database import Database
from modules.database_preset.domain.models.table import Table


class TableManagementService:
    def __init__(self, session):
        self.session = session

    @authorize_access(Database)
    def create(self, database_id: int, name: str, **kwargs) -> Table:
        with transaction_scope(self.session) as session:
            table, is_created = get_or_create(
                session,
                Table,
                database_id=database_id,
                name=name,
            )
            if is_created:
                table.update(**kwargs)
        return table

    @authorize_access(Table)
    def update(self, table_id: int, **kwargs) -> Table:
        with transaction_scope(self.session) as session:
            table = session.query(Table).get(table_id)
            table.update(**kwargs)
        return table

    @authorize_access(Table)
    def remove(self, table_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table = session.query(Table).get(table_id)
            session.delete(table)
        return True
