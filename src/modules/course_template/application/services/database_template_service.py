from instance_access import authorize_access
from models.utils import get_or_create, transaction_scope
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.database import DatabaseAssignmentTemplate


class DatabaseAssignmentTemplateManagementService:
    def __init__(self, session):
        self.session = session

    @authorize_access(AssignmentTemplate)
    def create(
        self, assignment_template_id: int, name: str, **kwargs
    ) -> DatabaseAssignmentTemplate:
        with transaction_scope(self.session) as session:
            is_database_exist = (
                session.query(DatabaseAssignmentTemplate)
                .filter(
                    DatabaseAssignmentTemplate.assignment_template_id
                    == assignment_template_id
                )
                .first()
            )

            if is_database_exist:
                raise Exception("Schema already defined for assignment template!")

            database, _ = get_or_create(
                session,
                DatabaseAssignmentTemplate,
                assignment_template_id=assignment_template_id,
                name=name,
            )
        return database

    @authorize_access(DatabaseAssignmentTemplate)
    def update(
        self, database_assignment_template_id: int, **kwargs
    ) -> DatabaseAssignmentTemplate:
        with transaction_scope(self.session) as session:
            database = session.query(DatabaseAssignmentTemplate).get(
                database_assignment_template_id
            )
            database.update(**kwargs)
        return database

    @authorize_access(DatabaseAssignmentTemplate)
    def remove(self, database_assignment_template_id: int, **kwargs) -> bool:
        with transaction_scope(self.session) as session:
            database = session.query(DatabaseAssignmentTemplate).get(
                database_assignment_template_id
            )
            session.delete(database)
        return True
