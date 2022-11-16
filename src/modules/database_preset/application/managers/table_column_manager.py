from sqlalchemy import and_, or_
from sqlalchemy.orm import Query

from models.utils import transaction_scope
from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.relation import TableRelation


class TableColumnManager:
    def __init__(self, session):
        self.session = session

    def get_relations(self, column: TableColumn) -> Query:
        with transaction_scope(self.session) as session:
            relations = session.query(TableRelation).filter(
                or_(
                    and_(
                        TableRelation.table_id == column.table_id,
                        TableRelation.table_column_name == column.name,
                    ),
                    and_(
                        TableRelation.relation_table_id == column.table_id,
                        TableRelation.relation_column_name == column.name,
                    ),
                )
            )
        return relations
