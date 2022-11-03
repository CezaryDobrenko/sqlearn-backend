import graphene

from api.graphql_api.schema.public import PublicQuery


class MeQuery(graphene.ObjectType):
    test = graphene.String()

    def resolve_test(self, info, **kwargs):
        return "im ok"


class Query(PublicQuery, MeQuery):
    node = graphene.Node.Field()
