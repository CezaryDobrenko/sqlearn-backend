from typing import Optional

from instance_access import authorize_access
from models.utils import transaction_scope
from modules.course_template.application.managers.data_template_manager import (
    TableDataAssignmentTemplateManager,
)
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.row import TableRowAssignmentTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate


class DataAssignmentTemplateManagementService:
    def __init__(self, session):
        self.session = session
        self.data_manager = TableDataAssignmentTemplateManager(session)

    @authorize_access(TableAssignmentTemplate)
    def create(
        self, table_assignment_template_id: int, row_data: list[list[str]], **kwargs
    ) -> list[TableColumnDataTemplate]:
        with transaction_scope(self.session) as session:
            table = session.query(TableAssignmentTemplate).get(
                table_assignment_template_id
            )

            row = TableRowAssignmentTemplate(
                ordinal=table.next_row_ordinal(),
                table_assignment_template=table,
            )
            session.add(row)

            for column in table.columns:
                value, _ = self._get_row_value(column, row_data)
                if self.data_manager.can_create(column, value):
                    cell = TableColumnDataTemplate(
                        table_column_assignment_template=column,
                        table_row_assignment_template=row,
                    )
                    cell.set_value(value)
                    session.add(cell)

        return row

    @authorize_access(TableRowAssignmentTemplate)
    def update_row(
        self,
        table_row_assignment_template_id: int,
        row_data: list[list[str]],
        **kwargs,
    ) -> TableColumnDataTemplate:
        with transaction_scope(self.session) as session:
            row = session.query(TableRowAssignmentTemplate).get(
                table_row_assignment_template_id
            )

            update_values = {}
            update_cells = []
            for cell in row.cells:
                cell_column = cell.table_column_assignment_template
                new_value, is_exist = self._get_row_value(cell_column, row_data)
                if is_exist:
                    update_values[f"{cell.id}"] = new_value
                    update_cells.append((cell, new_value))

            if row.on_update(session, **update_values):
                for cell, new_value in update_cells:
                    cell.set_value(new_value)

        return row

    @authorize_access(TableColumnDataTemplate)
    def update_cell(
        self,
        table_column_data_template_id: int,
        value: Optional[str],
        **kwargs,
    ) -> TableColumnDataTemplate:
        with transaction_scope(self.session) as session:
            cell = session.query(TableColumnDataTemplate).get(
                table_column_data_template_id
            )

            row = cell.table_row_assignment_template
            update_values = {f"{cell.id}": value}
            if row.on_update(session, **update_values):
                cell.set_value(value)

        return cell

    @authorize_access(TableRowAssignmentTemplate)
    def remove(self, table_row_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            row = session.query(TableRowAssignmentTemplate).get(
                table_row_assignment_template_id
            )
            if row.on_delete(session):
                session.delete(row)
        return True

    def _get_row_value(
        self, column: TableColumnAssignmentTemplate, row_data: list[list[str]]
    ) -> tuple[Optional[str], bool]:
        for row_item in row_data:
            item_name, item_value = row_item
            if item_name == column.name:
                return item_value, True
        return None, False
