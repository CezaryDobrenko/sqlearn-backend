from instance_access import authorize_access
from jwt_token import JWTService
from models.utils import get_or_create, transaction_scope
from modules.course_template.domain.models.course import CourseTemplate


class CourseTemplateManagementService:
    def __init__(self, session):
        self.session = session
        self.jwt_service = JWTService()

    def create(self, name: str, **kwargs) -> CourseTemplate:
        user = kwargs["current_user"]
        with transaction_scope(self.session) as session:
            course_template, is_created = get_or_create(
                session,
                CourseTemplate,
                owner_id=user.id,
                name=name,
            )
            if is_created:
                course_template.update(**kwargs)
        return course_template

    @authorize_access(CourseTemplate)
    def update(self, course_template_id: int, **kwargs) -> CourseTemplate:
        with transaction_scope(self.session) as session:
            course_template = session.query(CourseTemplate).get(course_template_id)
            course_template.update(**kwargs)
        return course_template

    @authorize_access(CourseTemplate)
    def remove(self, course_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            course_template = session.query(CourseTemplate).get(course_template_id)
            session.delete(course_template)
        return True

    @authorize_access(CourseTemplate)
    def publish(self, course_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            course_template = session.query(CourseTemplate).get(course_template_id)
            course_template.publish()
        return True

    @authorize_access(CourseTemplate)
    def withdraw(self, course_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            course_template = session.query(CourseTemplate).get(course_template_id)
            course_template.withdraw()
        return True
