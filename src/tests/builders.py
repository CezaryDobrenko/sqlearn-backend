from models import User
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.database_preset.domain.models.database import Database
from tests.factories import (
    DatabaseAssignmentTemplateFactory,
    DatabaseFactory,
    TableAssignmentTemplateFactory,
    TableColumnAssignmentTemplateFactory,
    TableColumnDataTemplateFactory,
    TableColumnFactory,
    TableFactory,
    TableRelationAssignmentTemplateFactory,
    TableRelationFactory,
)


def build_assignment_template_database(assignment_template: AssignmentTemplate):
    database = DatabaseAssignmentTemplateFactory(
        assignment_template=assignment_template
    )
    users_table = TableAssignmentTemplateFactory(
        database_assignment_template=database, name="users"
    )
    user_col_1 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=users_table, name="id"
    )
    user_col_2 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=users_table, name="name"
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_1, value=1
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_2, value="Mark"
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_1, value=2
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_2, value="Josh"
    )
    paintings_table = TableAssignmentTemplateFactory(
        database_assignment_template=database, name="paintings"
    )
    paint_col_1 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=paintings_table, name="id"
    )
    paint_col_2 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=paintings_table, name="name"
    )
    paint_col_3 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=paintings_table, name="user_id"
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_1, value=1
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_2, value="MonaLisa"
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_3, value=1
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_1, value=2
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_2, value="SunnyHills"
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_3, value=2
    )
    _ = TableRelationAssignmentTemplateFactory(
        name="old_fk",
        table=users_table,
        table_column_name="id",
        relation_table=paintings_table,
        relation_column_name="user_id",
    )
    return database


def build_preset_database(user: User) -> Database:
    preset_database = DatabaseFactory(user=user)
    users_table = TableFactory(database=preset_database, name="users")
    _ = TableColumnFactory(table=users_table, name="id")
    _ = TableColumnFactory(table=users_table, name="name")
    paintings_table = TableFactory(database=preset_database, name="paintings")
    _ = TableColumnFactory(table=paintings_table, name="id")
    _ = TableColumnFactory(table=paintings_table, name="name")
    _ = TableColumnFactory(table=paintings_table, name="user_id")
    warehouse_table = TableFactory(database=preset_database, name="warehouse")
    _ = TableColumnFactory(table=warehouse_table, name="id")
    _ = TableColumnFactory(table=warehouse_table, name="name")
    _ = TableColumnFactory(table=warehouse_table, name="painting_id")
    _ = TableRelationFactory(
        name="related_by_fk",
        table=users_table,
        table_column_name="id",
        relation_table=paintings_table,
        relation_column_name="user_id",
    )
    _ = TableRelationFactory(
        name="relation_fk",
        table=paintings_table,
        table_column_name="id",
        relation_table=warehouse_table,
        relation_column_name="painting_id",
    )
    return preset_database
