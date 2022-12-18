from instance_access import authorize_access
from models.utils import transaction_scope
from modules.course_template.application.managers.column_template_manager import (
    TableColumnAssignmentTemplateManager,
)
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
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
            current_rows_count = table.rows_count
            if self.column_manager.can_create(table, name, **kwargs):
                table_column = TableColumnAssignmentTemplate(
                    table_assignment_template=table,
                    name=name,
                    type=type,
                )
                table_column.update(**kwargs)
                session.add(table_column)
                session.commit()

                for _ in range(current_rows_count):
                    column_data = TableColumnDataTemplate(
                        table_column_assignment_template=table_column
                    )
                    column_data.set_value()

        return table_column

    @authorize_access(TableColumnAssignmentTemplate)
    def update(
        self, table_column_assignment_template_id: int, **kwargs
    ) -> TableColumnAssignmentTemplate:
        new_type = kwargs.get("type", None)
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumnAssignmentTemplate).get(
                table_column_assignment_template_id
            )
            if self.column_manager.can_update(table_column, **kwargs):
                previous_type = table_column.type
                table_column.update(**kwargs)

                if new_type and previous_type != new_type:
                    for cell in table_column.data:
                        cell.reset_value()

        return table_column

    @authorize_access(TableColumnAssignmentTemplate)
    def remove(self, table_column_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumnAssignmentTemplate).get(
                table_column_assignment_template_id
            )
            if self.column_manager.can_delete(table_column):
                session.delete(table_column)
        return True
