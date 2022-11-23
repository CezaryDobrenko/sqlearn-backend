from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.assignment_tag import AssignmentTemplateTag


class AssignmentTemplateTagManagementService:
    def __init__(self, session):
        self.session = session

    @authorize_access(AssignmentTemplate)
    def create(
        self, assignment_template_id: int, tag_id: int, **kwargs
    ) -> AssignmentTemplateTag:
        with transaction_scope(self.session) as session:
            assignment_template_tag, _ = get_or_create(
                session,
                AssignmentTemplateTag,
                assignment_template_id=assignment_template_id,
                tag_id=tag_id,
            )
        return assignment_template_tag

    @authorize_access(AssignmentTemplateTag)
    def remove(self, assignment_template_tag_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            assignment_template_tag = session.query(AssignmentTemplateTag).get(
                assignment_template_tag_id
            )
            session.delete(assignment_template_tag)
        return True
