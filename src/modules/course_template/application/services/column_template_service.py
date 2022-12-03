from exceptions import AlreadyExists, ColumnException
from instance_access import authorize_access
from models.utils import transaction_scope
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
        self, table_assignment_template_id: int, name: str, type: str, **kwargs
    ) -> TableColumnAssignmentTemplate:
        with transaction_scope(self.session) as session:
            table = session.query(TableAssignmentTemplate).get(
                table_assignment_template_id
            )
            if not self.column_manager.can_create(table, name):
                raise AlreadyExists("Column with that name is already defined!")

            table_column = TableColumnAssignmentTemplate(
                table_assignment_template_id=table_assignment_template_id,
                name=name,
                type=type,
            )
            table_column.update(**kwargs)
            session.add(table_column)

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
                raise ColumnException(action="update")

            table_column.update(**kwargs)
        return table_column

    @authorize_access(TableColumnAssignmentTemplate)
    def remove(self, table_column_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumnAssignmentTemplate).get(
                table_column_assignment_template_id
            )

            if not self.column_manager.can_delete(table_column):
                raise ColumnException(action="delete")

            session.delete(table_column)
        return True
