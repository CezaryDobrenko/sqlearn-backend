from exceptions import AlreadyExists, RelationException
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.helper.column_helper import (
    can_create_autoincrement_column,
    can_update_column_with_name,
)
from modules.helper.relation_helper import is_relation_exist


class TableColumnAssignmentTemplateManager:
    def __init__(self, session):
        self.session = session

    def can_create(self, table: TableAssignmentTemplate, name: str, **kwargs) -> bool:
        autoincrement = kwargs.get("is_autoincrement")

        if table.has_column(name):
            raise AlreadyExists("Column with given name already exist!")

        if not can_create_autoincrement_column(table, is_autoincrement=autoincrement):
            raise AlreadyExists("Autoincrement column already exist!")

        return True

    def can_update(self, column: TableColumnAssignmentTemplate, **kwargs) -> bool:
        exist = is_relation_exist(self.session, TableRelationAssignmentTemplate, column)
        table = column.table_assignment_template
        is_autoincrement = kwargs.get("is_autoincrement")

        if not can_update_column_with_name(table, column, kwargs.get("name")):
            raise AlreadyExists("Column with given name already exist!")

        if not can_create_autoincrement_column(table, column, is_autoincrement):
            raise AlreadyExists("Autoincrement column already exist!")

        if exist and column.is_relevant_field_updated(**kwargs):
            raise RelationException("At least one relation pointing at updated column!")

        return True

    def can_delete(self, column: TableColumnAssignmentTemplate) -> bool:
        if is_relation_exist(self.session, TableRelationAssignmentTemplate, column):
            raise RelationException("At least one relation pointing at updated column!")

        return True
