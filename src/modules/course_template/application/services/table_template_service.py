from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.course_template.domain.models.database import DatabaseAssignmentTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate


class TableAssignmentTemplateManagementService:
    def __init__(self, session):
        self.session = session

    @authorize_access(DatabaseAssignmentTemplate)
    def create(
        self, database_assignment_template_id: int, name: str, **kwargs
    ) -> DatabaseAssignmentTemplate:
        with transaction_scope(self.session) as session:
            assignment_table, is_created = get_or_create(
                session,
                TableAssignmentTemplate,
                database_assignment_template_id=database_assignment_template_id,
                name=name,
            )
            if is_created:
                assignment_table.update(**kwargs)
        return assignment_table

    @authorize_access(TableAssignmentTemplate)
    def update(
        self, table_assignment_template_id: int, **kwargs
    ) -> TableAssignmentTemplate:
        with transaction_scope(self.session) as session:
            assignment_table = session.query(TableAssignmentTemplate).get(
                table_assignment_template_id
            )
            assignment_table.update(**kwargs)
        return assignment_table

    @authorize_access(TableAssignmentTemplate)
    def remove(self, table_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            assignment_table = session.query(TableAssignmentTemplate).get(
                table_assignment_template_id
            )
            session.delete(assignment_table)
        return True
