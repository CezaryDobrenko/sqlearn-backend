from exceptions import AlreadyExists, RelationException
from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.course_template.application.managers.column_template_manager import (
    TableColumnAssignmentTemplateManager,
)
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate


class ColumnAssignmentTemplateManagementService:
    def __init__(self, session):
        self.session = session
        self.column_manager = TableColumnAssignmentTemplateManager(session)

    @authorize_access(TableAssignmentTemplate)
    def create(
        self, table_assignment_template_id: int, name: str, **kwargs
    ) -> TableColumnAssignmentTemplate:
        with transaction_scope(self.session) as session:
            table = session.query(TableAssignmentTemplate).get(
                table_assignment_template_id
            )
            if not self.column_manager.can_create(table, name):
                raise AlreadyExists("Column with that name is already defined!")

            table_column, is_created = get_or_create(
                session,
                TableColumnAssignmentTemplate,
                table_assignment_template_id=table_assignment_template_id,
                name=name,
            )
            if is_created:
                table_column.update(**kwargs)

            # TODO: add default data for existing rows

        return table_column

    @authorize_access(TableColumnAssignmentTemplate)
    def update(
        self, table_column_assignment_template_id: int, **kwargs
    ) -> TableColumnAssignmentTemplate:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumnAssignmentTemplate).get(
                table_column_assignment_template_id
            )

            if not self.column_manager.can_update(table_column, **kwargs):
                raise RelationException(action="update")

            table_column.update(**kwargs)
        return table_column

    @authorize_access(TableColumnAssignmentTemplate)
    def remove(self, table_column_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumnAssignmentTemplate).get(
                table_column_assignment_template_id
            )

            if not self.column_manager.can_delete(table_column):
                raise RelationException(action="delete")

            session.delete(table_column)
        return True
