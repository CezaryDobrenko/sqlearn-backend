import factory
from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from models import User
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.assignment_tag import AssignmentTemplateTag
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.column_data import TableColumnDataTemplate
from modules.course_template.domain.models.course import CourseTemplate
from modules.course_template.domain.models.database import DatabaseAssignmentTemplate
from modules.course_template.domain.models.quiz import QuizTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.row import TableRowAssignmentTemplate
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.course_template.domain.models.tag import Tag
from modules.database_preset.domain.models.column import ColumnType, TableColumn
from modules.database_preset.domain.models.database import Database
from modules.database_preset.domain.models.relation import RelationAction, TableRelation
from modules.database_preset.domain.models.table import Table


class UserFactory(SQLAlchemyModelFactory):
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")
    password = factory.PostGenerationMethodCall("set_password", "secret@pAs$word997")

    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"


class CourseTemplateFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"course-{n}")
    description = "course_description"
    owner = SubFactory(UserFactory)

    class Meta:
        model = CourseTemplate
        sqlalchemy_session_persistence = "flush"


class QuizTemplateFactory(SQLAlchemyModelFactory):
    title = factory.Sequence(lambda n: f"quiz-{n}")
    description = "quiz_description"
    course_template = SubFactory(CourseTemplateFactory)

    class Meta:
        model = QuizTemplate
        sqlalchemy_session_persistence = "flush"


class AssignmentTemplateFactory(SQLAlchemyModelFactory):
    title = factory.Sequence(lambda n: f"assignment-{n}")
    ordinal = factory.Sequence(lambda n: n)
    description = "assignment_description"
    quiz_template = SubFactory(QuizTemplateFactory)
    owner_solution = "SELECT * FROM users;"

    class Meta:
        model = AssignmentTemplate
        sqlalchemy_session_persistence = "flush"


class TagFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"tag-{n}")

    class Meta:
        model = Tag
        sqlalchemy_session_persistence = "flush"


class AssignmentTemplateTagFactory(SQLAlchemyModelFactory):
    assignment_template = SubFactory(AssignmentTemplateFactory)
    tag = SubFactory(TagFactory)

    class Meta:
        model = AssignmentTemplateTag
        sqlalchemy_session_persistence = "flush"


class DatabaseFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"database-{n}")
    user = SubFactory(UserFactory)

    class Meta:
        model = Database
        sqlalchemy_session_persistence = "flush"


class TableFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"table-{n}")
    description = "db_description"
    database = SubFactory(DatabaseFactory)

    class Meta:
        model = Table
        sqlalchemy_session_persistence = "flush"


class TableColumnFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"column-{n}")
    type = ColumnType.TEXT
    length = 200
    is_null = True
    table = SubFactory(TableFactory)

    class Meta:
        model = TableColumn
        sqlalchemy_session_persistence = "flush"


class TableRelationFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"column-{n}")
    action = RelationAction.CASCADE
    relation_column_name = "id"
    relation_table = SubFactory(TableFactory)
    table_column_name = "other_id"
    table = SubFactory(TableFactory)

    class Meta:
        model = TableRelation
        sqlalchemy_session_persistence = "flush"


class DatabaseAssignmentTemplateFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"database_assignment-{n}")
    assignment_template = SubFactory(AssignmentTemplateFactory)

    class Meta:
        model = DatabaseAssignmentTemplate
        sqlalchemy_session_persistence = "flush"


class TableAssignmentTemplateFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"table_assignment-{n}")
    description = "table_assignment_description"
    database_assignment_template = SubFactory(DatabaseAssignmentTemplateFactory)

    class Meta:
        model = TableAssignmentTemplate
        sqlalchemy_session_persistence = "flush"


class TableColumnAssignmentTemplateFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"column_assignment-{n}")
    type = ColumnType.TEXT
    length = 200
    is_null = True
    is_unique = True
    table_assignment_template = SubFactory(TableAssignmentTemplateFactory)

    class Meta:
        model = TableColumnAssignmentTemplate
        sqlalchemy_session_persistence = "flush"


class TableRelationAssignmentTemplateFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"relation_assignment-{n}")
    action = RelationAction.CASCADE
    relation_column_name = "id"
    relation_table = SubFactory(TableAssignmentTemplateFactory)
    table_column_name = "other_id"
    table = SubFactory(TableAssignmentTemplateFactory)

    class Meta:
        model = TableRelationAssignmentTemplate
        sqlalchemy_session_persistence = "flush"


class TableRowAssignmentTemplateFactory(SQLAlchemyModelFactory):
    table_assignment_template = SubFactory(TableAssignmentTemplateFactory)

    class Meta:
        model = TableRowAssignmentTemplate
        sqlalchemy_session_persistence = "flush"


class TableColumnDataTemplateFactory(SQLAlchemyModelFactory):
    value = factory.Sequence(lambda n: f"data-{n}")
    table_column_assignment_template = SubFactory(TableColumnAssignmentTemplateFactory)
    table_row_assignment_template = SubFactory(TableRowAssignmentTemplateFactory)

    class Meta:
        model = TableColumnDataTemplate
        sqlalchemy_session_persistence = "flush"
