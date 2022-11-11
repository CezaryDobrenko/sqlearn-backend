from graphene import relay

from api.graphql_api.authentication import get_user_by_token
from instance_access import has_user_access


class AuthorizedNode(relay.Node):
    class Meta:
        name = "AuthorizedNode"

    @classmethod
    def node_resolver(cls, only_type, root, info, id, **kwargs):
        current_user = get_user_by_token(info.context)
        instance = cls.get_node_from_global_id(info, id, only_type=only_type)
        try:
            return instance if has_user_access(instance, current_user) else None
        except NotImplementedError:
            return None
