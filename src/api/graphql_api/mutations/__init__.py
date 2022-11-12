import graphene

from .course import CourseMutation
from .quiz import QuizMutation
from .user import UserMutation


class Mutation(UserMutation, CourseMutation, QuizMutation, graphene.ObjectType):
    pass
