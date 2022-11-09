import graphene

from .course import CourseMutation
from .user import UserMutation


class Mutation(UserMutation, CourseMutation, graphene.ObjectType):
    pass
