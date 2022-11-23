import graphene

from .assignment import AssignmentTemplateMutation
from .assignment_tag import AssignmentTemplateTagMutation
from .column import TableColumnMutation
from .course import CourseMutation
from .database import DatabaseMutation
from .quiz import QuizMutation
from .relation import TableRelationMutation
from .table import TableMutation
from .user import UserMutation


class Mutation(
    AssignmentTemplateTagMutation,
    AssignmentTemplateMutation,
    CourseMutation,
    DatabaseMutation,
    QuizMutation,
    UserMutation,
    TableMutation,
    TableColumnMutation,
    TableRelationMutation,
    graphene.ObjectType,
):
    pass
