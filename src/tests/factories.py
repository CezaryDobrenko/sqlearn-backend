import factory
from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from models import User
from modules.course_template.domain.models.course import CourseTemplate
from modules.course_template.domain.models.quiz import QuizTemplate


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
