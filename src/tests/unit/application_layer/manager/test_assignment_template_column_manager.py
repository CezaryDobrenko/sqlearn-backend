import pytest

from exceptions import AlreadyExists, RelationException
from modules.course_template.application.services.column_template_service import (
    ColumnAssignmentTemplateManagementService,
)
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
