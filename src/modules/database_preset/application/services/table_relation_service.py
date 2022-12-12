from exceptions import RelationException
from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.database_preset.application.managers.table_relation_manager import (
    TableRelationManager,
)
from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table


class TableRelationManagementService:
    def __init__(self, session):
        self.session = session
        self.relation_manager = TableRelationManager(session)

    @authorize_access(Table)
    def create(
        self,
        table_id: int,
        relation_table_id: int,
        name: str,
        action: str,
        column_name: str,
        relation_column_name: str,
        **kwargs
    ) -> TableRelation:
        with transaction_scope(self.session) as session:
            if not self.relation_manager.can_create(
                table_id, column_name, relation_table_id, relation_column_name, **kwargs
            ):
                raise RelationException("create error")

            table_relation, _ = get_or_create(
                session,
                TableRelation,
                name=name,
                action=action,
                table_id=table_id,
                table_column_name=column_name,
                relation_table_id=relation_table_id,
                relation_column_name=relation_column_name,
            )
        return table_relation

    @authorize_access(TableRelation)
    def update(self, table_relation_id: int, **kwargs) -> TableRelation:
        with transaction_scope(self.session) as session:
            table_relation = session.query(TableRelation).get(table_relation_id)

            if not self.relation_manager.can_update(table_relation, **kwargs):
                raise RelationException("update error")

            table_relation.update(**kwargs)
        return table_relation

    @authorize_access(TableRelation)
    def remove(self, table_relation_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_relation = session.query(TableRelation).get(table_relation_id)
            session.delete(table_relation)
        return True
