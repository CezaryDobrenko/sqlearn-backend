from instance_access import has_user_access
from models.utils import transaction_scope
from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table
from modules.user.domain.models.user import User


class TableRelationManager:
    def __init__(self, session):
        self.session = session

    def can_create(
        self,
        source_table_id: int,
        source_column_name: str,
        relation_table_id: int,
        relation_column_name: str,
        **kwargs
    ) -> bool:
        user = kwargs["current_user"]
        with transaction_scope(self.session):
            is_source_valid = self._is_valid(source_table_id, source_column_name, user)
            is_relation_valid = self._is_valid(
                relation_table_id, relation_column_name, user
            )
        return True if is_source_valid and is_relation_valid else False

    def can_update(self, relation: TableRelation, **kwargs) -> bool:
        user = kwargs["current_user"]
        with transaction_scope(self.session):
            if "table_id" in kwargs:
                table_id = kwargs["relation_table_id"]
                source_column = (
                    relation.table_column_name
                    if "table_column_name" in kwargs
                    else kwargs["table_column_name"]
                )
                is_source_valid = self._is_valid(table_id, source_column, user)
            if "relation_table_id" in kwargs:
                relation_id = kwargs["relation_table_id"]
                relation_column = (
                    relation.relation_column_name
                    if "relation_column_name" in kwargs
                    else kwargs["relation_column_name"]
                )
                is_relation_valid = self._is_valid(relation_id, relation_column, user)
        return True if is_source_valid and is_relation_valid else False

    def _is_valid(self, table_id: int, column_name: str, user: User) -> bool:
        table = self.session.query(Table).get(table_id)
        if has_user_access(table, user):
            return True if table.has_column(column_name) else False
        raise Exception("Permision Denied")
