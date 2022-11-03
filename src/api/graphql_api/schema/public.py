import graphene
from graphene.relay.node import to_global_id


class Public(graphene.ObjectType):
    id = graphene.ID()
    test = graphene.String()

    def resolve_test(self, info, **kwargs):
        return "im ok"


public_instance = Public(id=to_global_id("Public", 1))


class PublicQuery(graphene.ObjectType):
    public = graphene.Field(Public)

    def resolve_public(self, info):
        return public_instance
