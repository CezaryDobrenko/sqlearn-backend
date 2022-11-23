from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.course_template.domain.models.quiz import QuizTemplate


class QuizTemplateManagementService:
    def __init__(self, session):
        self.session = session

    def create(self, course_template_id: int, title: str, **kwargs) -> QuizTemplate:
        with transaction_scope(self.session) as session:
            quiz_template, is_created = get_or_create(
                session,
                QuizTemplate,
                course_template_id=course_template_id,
                title=title,
            )
            session.flush()
            if is_created:
                quiz_template.update(**kwargs)
        return quiz_template

    @authorize_access(QuizTemplate)
    def update(self, quiz_template_id: int, **kwargs) -> QuizTemplate:
        with transaction_scope(self.session) as session:
            quiz_template = session.query(QuizTemplate).get(quiz_template_id)
            quiz_template.update(**kwargs)
        return quiz_template

    @authorize_access(QuizTemplate)
    def remove(self, quiz_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            quiz_template = session.query(QuizTemplate).get(quiz_template_id)
            session.delete(quiz_template)
        return True
