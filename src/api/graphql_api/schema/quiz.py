from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from api.graphql_api.connection import ExtendedConnection
from api.graphql_api.node import AuthorizedNode
from modules.course_template.domain.models.assignment import AssignmentTemplate
from modules.course_template.domain.models.quiz import QuizTemplate

from .assignment import AssignmentTemplateNode


class QuizTemplateNode(SQLAlchemyObjectType):
    class Meta:
        model = QuizTemplate
        interfaces = (AuthorizedNode,)
        connection_class = ExtendedConnection

    assignments_templates = SQLAlchemyConnectionField(AssignmentTemplateNode)

    def resolve_assignments_templates(self, info, **kwargs):
        return self.assignments_templates.order_by(AssignmentTemplate.ordinal)
