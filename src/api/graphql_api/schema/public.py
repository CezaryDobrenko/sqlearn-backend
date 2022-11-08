import graphene
from graphene.relay.node import to_global_id


class Public(graphene.ObjectType):
    id = graphene.ID()
    courses = graphene.String()

    def resolve_courses(self, info, **kwargs):
        return "im ok"


class PublicQuery(graphene.ObjectType):
    public = graphene.Field(Public)

    def resolve_public(self, info):
        return Public(id=to_global_id("Public", 1))
