from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table
from modules.helper.relation_helper import is_relation_exist


class TableColumnManager:
    def __init__(self, session):
        self.session = session

    def can_create(self, table_assignment_template: Table, name: str):
        for column in table_assignment_template.columns:
            if column.name == name:
                return False
        return True

    def can_update(self, column: TableColumn, **kwargs) -> bool:
        exist = is_relation_exist(self.session, TableRelation, column)
        if exist and column.is_relevant_field_updated(**kwargs):
            return False
        return True

    def can_delete(self, column: TableColumn) -> bool:
        exist = is_relation_exist(self.session, TableRelation, column)
        return False if exist else True
