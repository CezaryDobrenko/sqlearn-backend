from typing import Optional

from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.database import DatabaseAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.database import Database
from modules.database_preset.domain.models.table import Table

BASE_DATABASE = Database | DatabaseAssignmentTemplate


class DatabaseTemplateManager:
    def __init__(self, session):
        self.session = session

    def create_assignment_database(
        self,
        base_database: Optional[BASE_DATABASE],
        assignment_template: AssignmentTemplate,
        copy_data: bool,
    ) -> DatabaseAssignmentTemplate:
        if base_database:
            assignment_database, table_mapper = self._copy_database_schema(
                base_database,
                assignment_template,
                copy_data,
            )
            relations = self._copy_database_relations(base_database, table_mapper)
            for assignment_relation, _ in relations:
                self.session.add(assignment_relation)
        else:
            assignment_database = DatabaseAssignmentTemplate(
                name="Database", assignment_template=assignment_template
            )
        return assignment_database

    def _copy_database_schema(
        self,
        base_database: BASE_DATABASE,
        assignment_template: AssignmentTemplate,
        copy_data: bool,
    ) -> tuple[DatabaseAssignmentTemplate, dict]:
        table_mapper = {}
        assignment_database = DatabaseAssignmentTemplate(
            name=base_database.name, assignment_template=assignment_template
        )
        for assignment_table, base_table in self._copy_database_tables(
            base_database, assignment_database
        ):
            self.session.add(assignment_table)
            for assignment_column, base_column in self._copy_database_columns(
                base_table, assignment_table
            ):
                self.session.add(assignment_column)
                if copy_data:
                    for assignment_data, _ in self._copy_database_data(
                        base_column, assignment_column
                    ):
                        self.session.add(assignment_data)
            self.session.flush()
            table_mapper[f"{base_table.id}"] = assignment_table.id
        return assignment_database, table_mapper

    def _copy_database_relations(
        self, base_database: BASE_DATABASE, table_mapper: dict
    ) -> list[tuple]:
        relations = []
        for base_table in base_database.tables:
            for base_relation in base_table.relations:
                assignment_relation = TableRelationAssignmentTemplate(
                    name=base_relation.name,
                    action=base_relation.action.value,
                    relation_column_name=base_relation.relation_column_name,
                    relation_table_id=table_mapper[
                        f"{base_relation.relation_table_id}"
                    ],
                    table_column_name=base_relation.table_column_name,
                    table_id=table_mapper[f"{base_relation.table_id}"],
                )
                self.session.add(assignment_relation)
                relations.append((assignment_relation, base_relation))
        return relations

    def _copy_database_tables(
        self,
        base_database: BASE_DATABASE,
        assignment_database: DatabaseAssignmentTemplate,
    ) -> list[tuple]:
        tables = []
        for base_table in base_database.tables:
            assignment_table = TableAssignmentTemplate(
                name=base_table.name,
                description=base_table.description,
                database_assignment_template=assignment_database,
            )
            tables.append((assignment_table, base_table))
        return tables

    def _copy_database_columns(
        self,
        base_table: Table,
        assignment_table: TableAssignmentTemplate,
    ) -> list[tuple]:
        columns = []
        for base_column in base_table.columns:
            assignment_column = TableColumnAssignmentTemplate(
                name=base_column.name,
                type=base_column.type.value,
                length=base_column.length,
                is_null=base_column.is_null,
                is_unique=base_column.is_unique,
                table_assignment_template=assignment_table,
            )
            columns.append((assignment_column, base_column))
        return columns

    def _copy_database_data(
        self,
        base_column: TableColumnAssignmentTemplate,
        assignment_column: AssignmentTemplate,
    ) -> list[tuple]:
        data = []
        for base_data in base_column.data:
            assignment_data = TableColumnDataTemplate(
                value=base_data.value,
                table_column_assignment_template=assignment_column,
            )
            data.append((assignment_data, base_data))
        return data
