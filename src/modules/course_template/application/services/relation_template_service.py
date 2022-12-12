from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.course_template.application.managers.relation_template_manager import (
    TableRelationAssignmentTemplateManager,
)
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate


class TableRelationAssignmentTemplateManagementService:
    def __init__(self, session):
        self.session = session
        self.relation_manager = TableRelationAssignmentTemplateManager(session)

    @authorize_access(TableAssignmentTemplate)
    def create(
        self,
        table_assignment_template_id: int,
        relation_table_id: int,
        name: str,
        action: str,
        column_name: str,
        relation_column_name: str,
        **kwargs
    ) -> TableRelationAssignmentTemplate:
        with transaction_scope(self.session) as session:
            if self.relation_manager.can_create(
                table_assignment_template_id,
                column_name,
                relation_table_id,
                relation_column_name,
                **kwargs
            ):
                table_relation, _ = get_or_create(
                    session,
                    TableRelationAssignmentTemplate,
                    name=name,
                    action=action,
                    table_id=table_assignment_template_id,
                    table_column_name=column_name,
                    relation_table_id=relation_table_id,
                    relation_column_name=relation_column_name,
                )
        return table_relation

    @authorize_access(TableRelationAssignmentTemplate)
    def update(
        self, table_relation_assignment_template_id: int, **kwargs
    ) -> TableRelationAssignmentTemplate:
        with transaction_scope(self.session) as session:
            table_relation = session.query(TableRelationAssignmentTemplate).get(
                table_relation_assignment_template_id
            )

            if self.relation_manager.can_update(table_relation, **kwargs):
                table_relation.update(**kwargs)
        return table_relation

    @authorize_access(TableRelationAssignmentTemplate)
    def remove(self, table_relation_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_relation = session.query(TableRelationAssignmentTemplate).get(
                table_relation_assignment_template_id
            )
            session.delete(table_relation)
        return True
