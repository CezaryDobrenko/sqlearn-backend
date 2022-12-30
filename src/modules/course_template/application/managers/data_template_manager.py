from typing import Optional

from exceptions import AlreadyExists, InvalidValue
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.helper.column_helper import can_convert_value


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
