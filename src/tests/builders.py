from models import User
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.database import Database
from tests.factories import (
    AssignmentTemplateFactory,
    ColumnType,
    CourseTemplateFactory,
    DatabaseAssignmentTemplateFactory,
    DatabaseFactory,
    QuizTemplateFactory,
    TableAssignmentTemplateFactory,
    TableColumnAssignmentTemplateFactory,
    TableColumnDataTemplateFactory,
    TableColumnFactory,
    TableFactory,
    TableRelationAssignmentTemplateFactory,
    TableRelationFactory,
    TableRowAssignmentTemplateFactory,
)


def build_assignment_template(user: User):
    course_template = CourseTemplateFactory(owner=user)
    quiz_template = QuizTemplateFactory(course_template=course_template)
    assignment_template = AssignmentTemplateFactory(quiz_template=quiz_template)
    return assignment_template


def build_assignment_template_database(assignment_template: AssignmentTemplate):
    database = DatabaseAssignmentTemplateFactory(
        assignment_template=assignment_template
    )
    users_table = TableAssignmentTemplateFactory(
        database_assignment_template=database, name="users", autoincrement_index=3
    )
    user_col_1 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=users_table,
        name="id",
        is_autoincrement=True,
        type=ColumnType.INTEGER,
    )
    user_col_2 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=users_table, name="name", type=ColumnType.TEXT
    )
    user_row_1 = TableRowAssignmentTemplateFactory(
        table_assignment_template=users_table, ordinal=1
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_1,
        table_row_assignment_template=user_row_1,
        value=1,
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_2,
        table_row_assignment_template=user_row_1,
        value="Mark",
    )
    user_row_2 = TableRowAssignmentTemplateFactory(
        table_assignment_template=users_table, ordinal=2
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_1,
        table_row_assignment_template=user_row_2,
        value=2,
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=user_col_2,
        table_row_assignment_template=user_row_2,
        value="Josh",
    )
    paintings_table = TableAssignmentTemplateFactory(
        database_assignment_template=database, name="paintings", autoincrement_index=3
    )
    paint_col_1 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=paintings_table,
        name="id",
        is_autoincrement=True,
        type=ColumnType.INTEGER,
    )
    paint_col_2 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=paintings_table, name="name", type=ColumnType.TEXT
    )
    paint_col_3 = TableColumnAssignmentTemplateFactory(
        table_assignment_template=paintings_table,
        name="user_id",
        type=ColumnType.INTEGER,
    )
    paint_row_1 = TableRowAssignmentTemplateFactory(
        table_assignment_template=paintings_table, ordinal=1
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_1,
        table_row_assignment_template=paint_row_1,
        value=1,
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_2,
        table_row_assignment_template=paint_row_1,
        value="MonaLisa",
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_3,
        table_row_assignment_template=paint_row_1,
        value=1,
    )
    paint_row_2 = TableRowAssignmentTemplateFactory(
        table_assignment_template=paintings_table, ordinal=2
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_1,
        table_row_assignment_template=paint_row_2,
        value=2,
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_2,
        table_row_assignment_template=paint_row_2,
        value="SunnyHills",
    )
    _ = TableColumnDataTemplateFactory(
        table_column_assignment_template=paint_col_3,
        table_row_assignment_template=paint_row_2,
        value=2,
    )
    _ = TableRelationAssignmentTemplateFactory(
        name="old_fk",
        table=users_table,
        table_column_name="id",
        relation_table=paintings_table,
        relation_column_name="user_id",
    )
    return database


def build_assignment_template_table(
    database: DatabaseAssignmentTemplateFactory,
) -> TableAssignmentTemplate:
    warehourse_table = TableAssignmentTemplateFactory(
        database_assignment_template=database, name="warehouse"
    )
    _ = TableColumnAssignmentTemplateFactory(
        table_assignment_template=warehourse_table, name="id"
    )
    _ = TableColumnAssignmentTemplateFactory(
        table_assignment_template=warehourse_table, name="name"
    )
    return warehourse_table


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
