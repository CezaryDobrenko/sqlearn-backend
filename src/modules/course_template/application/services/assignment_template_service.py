from typing import Optional

from instance_access import authorize_access
from models.utils import transaction_scope
from modules.course_template.application.managers.database_template_manager import (
    DatabaseTemplateManager,
)
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.quiz import QuizTemplate
from modules.database_preset.domain.models.database import Database


class AssignmentTemplateManagementService:
    def __init__(self, session):
        self.session = session
        self.database_manager = DatabaseTemplateManager(session)

    @authorize_access(QuizTemplate)
    def create(self, quiz_template_id: int, title: str, **kwargs) -> AssignmentTemplate:
        with transaction_scope(self.session) as session:
            quiz_template = session.query(QuizTemplate).get(quiz_template_id)
            last_assignment = quiz_template.assignments_templates.order_by(
                AssignmentTemplate.ordinal.desc()
            ).first()
            ordinal = last_assignment.ordinal + 1 if last_assignment else 1

            assignment_template = AssignmentTemplate(
                quiz_template_id=quiz_template_id,
                title=title,
                ordinal=ordinal,
                description=kwargs.get("description"),
                owner_solution=kwargs.get("owner_solution"),
            )
            session.add(assignment_template)
            prev_database, copy_data = (
                (last_assignment.database, True) if last_assignment else (None, False)
            )
            self.database_manager.create_assignment_database(
                prev_database, assignment_template, copy_data
            )
        return assignment_template

    @authorize_access(AssignmentTemplate)
    def update(
        self, assignment_template_id: int, database_id: Optional[int], **kwargs
    ) -> AssignmentTemplate:
        with transaction_scope(self.session) as session:
            assignment_template = session.query(AssignmentTemplate).get(
                assignment_template_id
            )
            assignment_template.update(**kwargs)
            if database_id:
                session.delete(assignment_template.database)
                session.commit()
                base_database = session.query(Database).get(database_id)
                self.database_manager.create_assignment_database(
                    base_database, assignment_template, False
                )
        return assignment_template

    @authorize_access(AssignmentTemplate)
    def remove(self, assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            assignment_template = session.query(AssignmentTemplate).get(
                assignment_template_id
            )
            if assignment_template.database:
                session.delete(assignment_template.database)
            session.delete(assignment_template)
        return True
