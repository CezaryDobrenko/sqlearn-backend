import pytest

from exceptions import AlreadyExists, InvalidValue, RelationException
from modules.course_template.application.services.column_template_service import (
    ColumnAssignmentTemplateManagementService,
)
from modules.database_preset.domain.models.column import ColumnType
from tests.builders import build_assignment_template_database


def test_update_column_with_name_already_taken_by_other_column(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, _, column = table.columns.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(AlreadyExists):
        update = {"current_user": user, "name": "name"}
        service.update(column.id, **update)


def test_update_column_with_name_already_taken_by_updated_column(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, _, column = table.columns.all()

    update = {"current_user": user, "name": "user_id"}
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.update(column.id, **update)


def test_update_column_with_autoincrement_already_defined_by_other_column(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, _, column = table.columns.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(AlreadyExists):
        update = {"current_user": user, "is_autoincrement": True}
        service.update(column.id, **update)


def test_update_column_with_autoincrement_already_defined_by_updated_column(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    column, _, _ = table.columns.all()

    update = {"current_user": user, "is_autoincrement": True}
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.update(column.id, **update)


def test_update_relevant_data_in_column_with_defined_relation(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, _, column = table.columns.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(RelationException):
        update = {"current_user": user, "name": "other_id"}
        service.update(column.id, **update)


def test_update_irrelevant_data_in_column_with_defined_relation(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, _, column = table.columns.all()

    update = {"current_user": user, "is_null": True}
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.update(column.id, **update)


def test_update_column_with_type_convertable_with_default_value(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, column, _ = table.columns.all()

    update = {"current_user": user, "type": "BLOB", "default_value": "test"}
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.update(column.id, **update)


def test_update_column_with_type_not_convertable_with_default_value(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, column, _ = table.columns.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(InvalidValue):
        update = {"current_user": user, "type": "INTEGER", "default_value": "test"}
        service.update(column.id, **update)


def test_update_column_with_type_convertable_data(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, column, _ = table.columns.all()

    update = {"current_user": user, "type": "BLOB", "default_value": "test"}
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.update(column.id, **update)


def test_update_column_with_type_not_convertable_data(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, column, _ = table.columns.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(InvalidValue):
        update = {"current_user": user, "type": "INTEGER", "default_value": "0"}
        service.update(column.id, **update)


def test_update_column_with_is_unique_when_data_is_unique(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, col_2, _ = table.columns.all()

    update = {"current_user": user, "is_unique": True}
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.update(col_2.id, **update)


def test_update_column_with_is_unique_when_data_is_not_unique(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    table_column_data_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    col_1, col_2, col_3 = table.columns.all()
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_1, value=3
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_2, value="MonaLisa"
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_3, value=2
    )

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(InvalidValue):
        update = {"current_user": user, "is_unique": True}
        service.update(col_2.id, **update)


def test_update_column_with_is_null_when_data_contain_null_values(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    table_column_data_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    col_1, col_2, col_3 = table.columns.all()
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_1, value=3
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_2, value=None
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_3, value=2
    )

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(InvalidValue):
        update = {"current_user": user, "is_null": False}
        service.update(col_2.id, **update)


def test_update_column_with_autoincrement_attribute(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    database_assignment_template_factory,
    table_assignment_template_factory,
    table_column_assignment_template_factory,
    table_column_data_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database = database_assignment_template_factory(
        assignment_template=assignment_template
    )
    table = table_assignment_template_factory(
        database_assignment_template=database, name="users", autoincrement_index=9
    )
    col_1 = table_column_assignment_template_factory(
        table_assignment_template=table,
        name="id",
        is_autoincrement=False,
        type=ColumnType.INTEGER,
    )
    col_2 = table_column_assignment_template_factory(
        table_assignment_template=table, name="name", type=ColumnType.TEXT
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_1, value=1
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_2, value="Mark"
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_1, value=5
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_2, value="Josh"
    )

    update = {"current_user": user, "is_autoincrement": True}
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.update(col_1.id, **update)

    assert col_1.is_autoincrement is True
    assert table.autoincrement_index == 6


def test_create_column_with_name_already_taken_by_other_column(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(AlreadyExists):
        update = {"current_user": user, "name": "name", "type": "INTEGER"}
        service.create(table.id, **update)


def test_create_column_with_autoincrement_when_is_already_defined_for_other_column(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(AlreadyExists):
        update = {
            "current_user": user,
            "name": "name",
            "type": "INTEGER",
            "is_autoincrement": True,
        }
        service.create(table.id, **update)


def test_create_column_with_autoincrement(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    database_assignment_template_factory,
    table_assignment_template_factory,
    table_column_assignment_template_factory,
    table_column_data_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database = database_assignment_template_factory(
        assignment_template=assignment_template
    )
    table = table_assignment_template_factory(
        database_assignment_template=database, name="users", autoincrement_index=1
    )
    col_1 = table_column_assignment_template_factory(
        table_assignment_template=table,
        name="pesel",
        is_autoincrement=False,
        type=ColumnType.INTEGER,
    )
    col_2 = table_column_assignment_template_factory(
        table_assignment_template=table, name="name", type=ColumnType.TEXT
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_1, value="98020192741"
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_2, value="Mark"
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_1, value="98020192742"
    )
    _ = table_column_data_template_factory(
        table_column_assignment_template=col_2, value="Josh"
    )

    update = {
        "current_user": user,
        "name": "new_id",
        "type": "INTEGER",
        "is_autoincrement": True,
    }
    service = ColumnAssignmentTemplateManagementService(db_session)
    service.create(table.id, **update)

    column_names = [column.name for column in table.columns.all()]
    _, _, new_column = table.columns.all()
    cell_values = [cell.value for cell in new_column.data.all()]
    assert table.columns.count() == 3
    assert column_names == ["pesel", "name", "new_id"]
    assert cell_values == ["1", "2"]


def test_delete_column_when_relation_exist(
    user_factory,
    db_session,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    database_template = build_assignment_template_database(assignment_template)
    _, table = database_template.tables.all()
    _, _, column = table.columns.all()

    service = ColumnAssignmentTemplateManagementService(db_session)

    with pytest.raises(RelationException):
        service.remove(column.id, **{"current_user": user})
