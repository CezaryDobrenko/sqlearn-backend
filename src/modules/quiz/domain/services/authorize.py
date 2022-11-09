from instance_access import has_user_access
from modules.quiz.domain.models.course import CourseTemplate
from modules.user.domain.models.user import User


@has_user_access.register(CourseTemplate)
def _has_user_access_course_template(instance: CourseTemplate, user: User) -> bool:
    return instance.owner == user
