from exceptions import AlreadyExists, InvalidValue, RelationException
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.helper.column_helper import (
    can_create_autoincrement_column,
    can_update_column_with_name,
    is_default_value_valid_type,
)
from modules.helper.relation_helper import is_relation_exist


class TableColumnAssignmentTemplateManager:
    def __init__(self, session):
        self.session = session

    def can_create(self, table: TableAssignmentTemplate, name: str, **kwargs) -> bool:
        autoincrement = kwargs.get("is_autoincrement")
        default_value = kwargs.get("default_value")
        column_type = kwargs.get("type")

        if table.has_column(name):
            raise AlreadyExists("Column with given name already exist!")

        if not can_create_autoincrement_column(table, is_autoincrement=autoincrement):
            raise AlreadyExists("Autoincrement column already exist!")

        if not is_default_value_valid_type(column_type, default_value):
            raise InvalidValue("Default value is not valid with given type of column")

        return True

    def can_update(self, column: TableColumnAssignmentTemplate, **kwargs) -> bool:
        exist = is_relation_exist(self.session, TableRelationAssignmentTemplate, column)
        table = column.table_assignment_template
        is_autoincrement = kwargs.get("is_autoincrement")
        new_default = kwargs.get("default_value")
        new_type = kwargs.get("type")
        column_type = new_type if new_type else column.type.value
        default_value = new_default if new_default else column.default_value

        if not can_update_column_with_name(table, column, kwargs.get("name")):
            raise AlreadyExists("Column with given name already exist!")

        if not can_create_autoincrement_column(table, column, is_autoincrement):
            raise AlreadyExists("Autoincrement column already exist!")

        if exist and column.is_relevant_field_updated(**kwargs):
            raise RelationException("At least one relation pointing at updated column!")

        if not is_default_value_valid_type(column_type, default_value):
            raise InvalidValue("Default value is not valid with given type of column")

        return True

    def can_delete(self, column: TableColumnAssignmentTemplate) -> bool:
        if is_relation_exist(self.session, TableRelationAssignmentTemplate, column):
            raise RelationException("At least one relation pointing at updated column!")

        return True
