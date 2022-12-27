from typing import Optional

from exceptions import AlreadyExists, InvalidValue, RelationException
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.database_preset.domain.models.column import ColumnType
from modules.helper.column_helper import (
    can_convert_value,
    can_create_autoincrement_column,
    can_update_column_with_name,
)
from modules.helper.relation_helper import get_relations


class TableDataAssignmentTemplateManager:
    def __init__(self, session):
        self.session = session

    def can_create(
        self, column: TableColumnAssignmentTemplate, value: Optional[str]
    ) -> bool:
        if not can_convert_value(column.type.value, value):
            raise InvalidValue(
                f"Given value: {value} is not vaild for column type: {column.type.value}"
            )

        if (column.is_autoincrement or column.is_unique) and value:
            if column.is_value_already_defined(value):
                raise AlreadyExists(f"Given {value} is already defined in {column}")

        for relation in column.table_assignment_template.relations:
            if relation.source_column == column:
                if not relation.relation_column.is_value_already_defined(value):
                    raise InvalidValue(
                        f"Related table {relation.relation_table.name} doesn't contain {value} in {relation.relation_column.name}"
                    )
        return True
