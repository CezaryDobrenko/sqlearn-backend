from typing import Optional

from exceptions import InvalidValue
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


def is_default_value_valid_type(column_type: str, default_value: str) -> bool:
    if column_type and default_value:
        try:
            if column_type in ["INTEGER", "NUMERIC"]:
                int(default_value)
            elif column_type in ["TEXT", "BLOB"]:
                str(default_value)
            elif column_type == "REAL":
                float(default_value)
            else:
                raise InvalidValue("Unexpected column type")
            return True
        except Exception:
            return False
    return True
