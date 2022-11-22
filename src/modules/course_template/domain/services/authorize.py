from instance_access import has_user_access
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.course import CourseTemplate
from modules.course_template.domain.models.quiz import QuizTemplate
from modules.user.domain.models.user import User


@has_user_access.register(CourseTemplate)
def _has_user_access_course_template(instance: CourseTemplate, user: User) -> bool:
    return instance.owner == user


@has_user_access.register(QuizTemplate)
def _has_user_access_quiz_template(instance: QuizTemplate, user: User) -> bool:
    return instance.course_template.owner == user


@has_user_access.register(AssignmentTemplate)
def _has_user_access_assignment_template(
    instance: AssignmentTemplate, user: User
) -> bool:
    return instance.quiz_template.course_template.owner == user
