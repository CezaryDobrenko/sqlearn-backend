from instance_access import authorize_access
from models.utils import transaction_scope
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.row import TableRowAssignmentTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate


class DataAssignmentTemplateManagementService:
    def __init__(self, session):
        self.session = session

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
                value = self._get_row_value(column, row_data)
                cell = TableColumnDataTemplate(
                    table_column_assignment_template=column,
                    table_row_assignment_template=row,
                )
                cell.set_value(value)
                session.add(cell)

        return row

    def _get_row_value(
        self, column: TableColumnAssignmentTemplate, row_data: list[list[str]]
    ) -> str:
        for row_item in row_data:
            item_name, item_value = row_item
            if item_name == column.name:
                return item_value
        return None
