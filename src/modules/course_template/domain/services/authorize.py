from instance_access import has_user_access
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
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.user.domain.models.user import User


@has_user_access.register(CourseTemplate)
def _has_user_access_course_template(instance: CourseTemplate, user: User) -> bool:
    return instance.owner == user


@has_user_access.register(QuizTemplate)
def _has_user_access_quiz_template(instance: QuizTemplate, user: User) -> bool:
    return has_user_access(instance.course_template, user)


@has_user_access.register(AssignmentTemplate)
def _has_user_access_assignment_template(
    instance: AssignmentTemplate, user: User
) -> bool:
    return has_user_access(instance.quiz_template, user)


@has_user_access.register(DatabaseAssignmentTemplate)
def _has_user_access_database_assignment_template(
    instance: DatabaseAssignmentTemplate, user: User
) -> bool:
    return has_user_access(instance.assignment_template, user)


@has_user_access.register(TableAssignmentTemplate)
def _has_user_access_table_assignment_template(
    instance: TableAssignmentTemplate, user: User
) -> bool:
    return has_user_access(instance.database_assignment_template, user)


@has_user_access.register(TableColumnAssignmentTemplate)
def _has_user_access_table_column_assignment_template(
    instance: TableColumnAssignmentTemplate, user: User
) -> bool:
    return has_user_access(instance.table_assignment_template, user)


@has_user_access.register(TableRelationAssignmentTemplate)
def _has_user_access_table_relation_assignment_template(
    instance: TableRelationAssignmentTemplate, user: User
) -> bool:
    return has_user_access(instance.table, user)


@has_user_access.register(TableColumnDataTemplate)
def _has_user_access_table_column_data_assignment_template(
    instance: TableColumnDataTemplate, user: User
) -> bool:
    return has_user_access(instance.table_column_assignment_template, user)


@has_user_access.register(AssignmentTemplateTag)
def _has_user_access_assignment_template_tag(
    instance: AssignmentTemplateTag, user: User
) -> bool:
    return has_user_access(instance.assignment_template, user)
