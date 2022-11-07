import graphene
from graphene import Connection


class ExtendedConnection(Connection):
    class Meta:
        abstract = True

    nodes_count = graphene.Int()
    edges_count = graphene.Int()

    def resolve_nodes_count(root, info, **kwargs):
        return root.length

    def resolve_edges_count(root, info, **kwargs):
        return len(root.edges)
