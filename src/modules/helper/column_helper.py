from typing import Optional

from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.table import Table

TABLE_MODEL = Table | TableAssignmentTemplate
COLUMN_MODEL = TableColumn | TableColumnAssignmentTemplate


def can_update_column_with_name(
    table: TABLE_MODEL,
    column: Optional[COLUMN_MODEL] = None,
    name: Optional[str] = None,
) -> bool:
    if name:
        table_column = table.get_column(name)
        if table_column and column != table_column:
            return False
    return True


def can_create_autoincrement_column(
    table: TABLE_MODEL,
    column: Optional[COLUMN_MODEL] = None,
    is_autoincrement: Optional[bool] = None,
) -> bool:
    if is_autoincrement:
        autoincrement_column = table.has_autoincrement_defined()
        if autoincrement_column and autoincrement_column != column:
            return False
    return True
