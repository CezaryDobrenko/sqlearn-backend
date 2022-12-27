import pytest

from exceptions import RelationException
from modules.course_template.application.services.relation_template_service import (
    TableRelationAssignmentTemplateManagementService,
)
from tests.builders import build_assignment_template_database


def test_create_relation_when_already_defined(
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
    source_table, destination_table = database_template.tables.all()
    src_column, _ = source_table.columns.all()
    _, _, dest_column = destination_table.columns.all()

    service = TableRelationAssignmentTemplateManagementService(db_session)

    with pytest.raises(RelationException):
        kwargs = {"current_user": user}
        service.create(
            destination_table.id,
            source_table.id,
            "new_name",
            "CASCADE",
            dest_column.name,
            src_column.name,
            **kwargs
        )


def test_create_relation_with_invalid_source_column_data(
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
    source_table, destination_table = database_template.tables.all()
    _, _, dest_column = destination_table.columns.all()

    service = TableRelationAssignmentTemplateManagementService(db_session)

    with pytest.raises(RelationException):
        kwargs = {"current_user": user}
        service.create(
            source_table.id,
            destination_table.id,
            "new_name",
            "CASCADE",
            "invalid_column_name",
            dest_column.name,
            **kwargs
        )


def test_create_relation_with_invalid_source_data(
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
    source_table, destination_table = database_template.tables.all()
    src_column, _ = source_table.columns.all()

    service = TableRelationAssignmentTemplateManagementService(db_session)

    with pytest.raises(RelationException):
        kwargs = {"current_user": user}
        service.create(
            source_table.id,
            destination_table.id,
            "new_name",
            "CASCADE",
            src_column.name,
            "invalid_column_name",
            **kwargs
        )


def test_update_relation_with_unmodified_data(
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
    _, relation_table = database_template.tables.all()
    relation = relation_table.relations.first()

    update = {
        "current_user": user,
        "name": relation.name,
        "action": relation.action,
        "source_column_name": relation.table_column_name,
        "source_table_id": relation.table_id,
        "relation_column_name": relation.relation_column_name,
        "relation_table_id": relation.relation_table_id,
    }
    service = TableRelationAssignmentTemplateManagementService(db_session)
    service.update(relation.id, **update)
