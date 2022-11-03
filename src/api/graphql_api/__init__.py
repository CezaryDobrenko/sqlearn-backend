import graphene

from .mutations import Mutation
from .schema import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
