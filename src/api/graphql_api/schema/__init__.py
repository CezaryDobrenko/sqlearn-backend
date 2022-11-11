import graphene

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.public import PublicQuery

from .user import UserNode
from api.graphql_api.node import AuthorizedNode


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserNode)

    @authentication_required()
    def resolve_user(self, info, **kwargs):
        return kwargs["current_user"]


class Query(PublicQuery, UserQuery):
    node = graphene.Node.Field()
    authorized_node = AuthorizedNode.Field()
