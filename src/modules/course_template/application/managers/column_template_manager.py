from sqlalchemy import and_, or_
from sqlalchemy.orm import Query

from models.utils import transaction_scope
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)


class TableColumnAssignmentTemplateManager:
    def __init__(self, session):
        self.session = session

    def get_relations(self, column: TableColumnAssignmentTemplate) -> Query:
        with transaction_scope(self.session) as session:
            relations = session.query(TableRelationAssignmentTemplate).filter(
                or_(
                    and_(
                        TableRelationAssignmentTemplate.table_id
                        == column.table_assignment_template_id,
                        TableRelationAssignmentTemplate.table_column_name
                        == column.name,
                    ),
                    and_(
                        TableRelationAssignmentTemplate.relation_table_id
                        == column.table_assignment_template_id,
                        TableRelationAssignmentTemplate.relation_column_name
                        == column.name,
                    ),
                )
            )
        return relations
