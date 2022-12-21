from typing import Optional

from exceptions import AlreadyExists, InvalidValue, RelationException
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.column import ColumnType
from modules.helper.column_helper import (
    can_convert_value,
    can_create_autoincrement_column,
    can_update_column_with_name,
)
from modules.helper.relation_helper import is_relation_exist


class TableColumnAssignmentTemplateManager:
    def __init__(self, session):
        self.session = session

    def can_create(
        self,
        table: TableAssignmentTemplate,
        name: str,
        type: str,
        is_autoincrement: Optional[bool] = None,
        default_value: Optional[str] = None,
    ) -> bool:
        if table.has_column(name):
            raise AlreadyExists("Column with given name already exist!")

        if not can_create_autoincrement_column(
            table, is_autoincrement=is_autoincrement
        ):
            raise AlreadyExists("Autoincrement column already exist!")

        if not can_convert_value(type, default_value):
            raise InvalidValue("Default value is not valid with given type of column")

        return True

    def can_update(
        self,
        column: TableColumnAssignmentTemplate,
        column_name: str,
        column_type: str,
        default_value: str,
        is_autoincrement: bool,
        is_unique: bool,
        is_null: bool,
        is_relevant_updated_field: bool,
    ) -> bool:
        table = column.table_assignment_template
        exist = is_relation_exist(self.session, TableRelationAssignmentTemplate, column)

        if not can_update_column_with_name(table, column, column_name):
            raise AlreadyExists("Column with given name already exist!")

        if not can_create_autoincrement_column(table, column, is_autoincrement):
            raise AlreadyExists("Autoincrement column already exist!")

        if not can_convert_value(column_type, default_value):
            raise InvalidValue("Default value is not valid with given type of column")

        if exist and is_relevant_updated_field:
            raise RelationException("At least one relation pointing at updated column!")

        if not self._can_convert_existing_column_data(column_type, column):
            raise InvalidValue("Existing cells are not valid with given column type!")

        if is_autoincrement and column_type != ColumnType.INTEGER.value:
            raise InvalidValue("Only INTEGER type can have autoincrement attribute!")

        if is_null is False and self._is_existing_column_data_contain_null(column):
            raise InvalidValue("Existing cells are containing null values!")

        if is_autoincrement or is_unique:
            if not self._is_existing_column_data_unique(column):
                raise InvalidValue("Existing cells are not unique!")

        return True

    def can_delete(self, column: TableColumnAssignmentTemplate) -> bool:
        if is_relation_exist(self.session, TableRelationAssignmentTemplate, column):
            raise RelationException("At least one relation pointing at updated column!")

        return True

    def _can_convert_existing_column_data(
        self, column_type: str, column: TableColumnAssignmentTemplate
    ) -> bool:
        for cell in column.data:
            if not can_convert_value(column_type, cell.value):
                return False
        return True

    def _is_existing_column_data_unique(
        self, column: TableColumnAssignmentTemplate
    ) -> bool:
        values = []
        for cell in column.data:
            if cell.value in values:
                return False
            values.append(cell.value)
        return True

    def _is_existing_column_data_contain_null(
        self, column: TableColumnAssignmentTemplate
    ) -> bool:
        for cell in column.data:
            if cell.value is None:
                return True
        return False
