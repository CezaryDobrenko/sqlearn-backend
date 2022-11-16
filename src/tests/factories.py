import factory
from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from models import User
from modules.course_template.domain.models.course import CourseTemplate
from modules.course_template.domain.models.quiz import QuizTemplate
from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.database import Database
from modules.database_preset.domain.models.relation import TableRelation
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
    type = "TEXT"
    length = 200
    is_null = True
    table = SubFactory(TableFactory)

    class Meta:
        model = TableColumn
        sqlalchemy_session_persistence = "flush"


class TableRelationFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: f"column-{n}")
    action = "CASCADE"
    relation_column_name = "id"
    relation_table = SubFactory(TableFactory)
    table_column_name = "other_id"
    table = SubFactory(TableFactory)

    class Meta:
        model = TableRelation
        sqlalchemy_session_persistence = "flush"
