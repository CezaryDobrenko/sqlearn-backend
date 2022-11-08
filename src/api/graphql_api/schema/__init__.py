import graphene

from api.graphql_api.authentication import login_required
from api.graphql_api.schema.public import PublicQuery

from .user import UserNode


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserNode)

    @login_required()
    def resolve_user(self, info, **kwargs):
        return kwargs["current_user"]


class Query(PublicQuery, UserQuery):
    node = graphene.Node.Field()
