from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.database_preset.domain.models.database import Database


class DatabaseManagementService:
    def __init__(self, session):
        self.session = session

    def create(self, name: str, **kwargs) -> Database:
        user = kwargs["current_user"]
        with transaction_scope(self.session) as session:
            database, _ = get_or_create(
                session,
                Database,
                user_id=user.id,
                name=name,
            )
        return database

    @authorize_access(Database)
    def update(self, database_id: int, **kwargs) -> Database:
        with transaction_scope(self.session) as session:
            database = session.query(Database).get(database_id)
            database.update(**kwargs)
        return database

    @authorize_access(Database)
    def remove(self, database_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            database = session.query(Database).get(database_id)
            session.delete(database)
        return True
