from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.helper.relation_helper import is_relation_exist


class TableColumnAssignmentTemplateManager:
    def __init__(self, session):
        self.session = session

    def can_create(self, table_assignment_template: TableAssignmentTemplate, name: str):
        for column in table_assignment_template.columns:
            if column.name == name:
                return False
        return True

    def can_update(self, column: TableColumnAssignmentTemplate, **kwargs) -> bool:
        exist = is_relation_exist(self.session, TableRelationAssignmentTemplate, column)
        if exist and column.is_relevant_field_updated(**kwargs):
            return False
        return True

    def can_delete(self, column: TableColumnAssignmentTemplate) -> bool:
        exist = is_relation_exist(self.session, TableRelationAssignmentTemplate, column)
        return False if exist else True
