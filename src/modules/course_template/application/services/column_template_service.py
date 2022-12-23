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
        new_is_autoincrement = kwargs.get("is_autoincrement")
        new_default_value = kwargs.get("default_value")
        with transaction_scope(self.session) as session:
            table = session.query(TableAssignmentTemplate).get(
                table_assignment_template_id
            )
            if self.column_manager.can_create(
                table, name, type, new_is_autoincrement, new_default_value
            ):
                table_column = TableColumnAssignmentTemplate(
                    table_assignment_template=table,
                    name=name,
                    type=type,
                )
                table_column.update(**kwargs)
                session.add(table_column)
                session.commit()

                for table_row in table.rows:
                    column_data = TableColumnDataTemplate(
                        table_column_assignment_template=table_column,
                        table_row_assignment_template=table_row,
                    )
                    column_data.set_value()

        return table_column

    @authorize_access(TableColumnAssignmentTemplate)
    def update(
        self, table_column_assignment_template_id: int, **kwargs
    ) -> TableColumnAssignmentTemplate:
        new_is_autoincrement = kwargs.get("is_autoincrement")
        new_is_unique = kwargs.get("is_unique")
        new_is_null = kwargs.get("is_null")
        new_default_value = kwargs.get("default_value")
        new_type = kwargs.get("type")
        new_name = kwargs.get("name")
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumnAssignmentTemplate).get(
                table_column_assignment_template_id
            )
            is_relevant_updated_field = table_column.is_relevant_field_updated(**kwargs)

            column_name = table_column.name
            if new_name is not None:
                column_name = new_name

            column_type = table_column.type.value
            if new_type is not None:
                column_type = new_type

            default_value = table_column.default_value
            if new_default_value is not None:
                default_value = new_default_value

            is_unique = table_column.is_unique
            if new_is_unique is not None:
                is_unique = new_is_unique

            is_autoincrement = table_column.is_autoincrement
            if new_is_autoincrement is not None:
                is_autoincrement = new_is_autoincrement

            is_null = table_column.is_null
            if new_is_null is not None:
                is_null = new_is_null

            if self.column_manager.can_update(
                table_column,
                column_name,
                column_type,
                default_value,
                is_autoincrement,
                is_unique,
                is_null,
                is_relevant_updated_field,
            ):
                previous_is_autoincrement = table_column.is_autoincrement
                table_column.update(**kwargs)

                if previous_is_autoincrement is False and is_autoincrement is True:
                    max_id = self._get_max_id_from_column(table_column)
                    table_column.update_autoincrement_index(max_id + 1)

        return table_column

    @authorize_access(TableColumnAssignmentTemplate)
    def remove(self, table_column_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            table_column = session.query(TableColumnAssignmentTemplate).get(
                table_column_assignment_template_id
            )
            if self.column_manager.can_delete(table_column):
                if table_column.is_autoincrement:
                    table_column.table_assignment_template.reset_autoincrement_index()

                session.delete(table_column)
        return True

    def _get_max_id_from_column(
        self, table_column: TableColumnAssignmentTemplate
    ) -> int:
        max_id = 1
        for cell in table_column.data:
            current_id = int(cell.value)
            if current_id > max_id:
                max_id = current_id
        return max_id
