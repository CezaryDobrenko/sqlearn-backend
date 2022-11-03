import graphene

from .user import UserMutation


class Mutation(UserMutation, graphene.ObjectType):
    pass
