from typing import Optional

from graphene.relay.node import from_global_id


def retrieve_id(string_gid: str, class_name: Optional[str] = None) -> int:
    object_type, object_id = from_global_id(string_gid)
    if object_type != class_name and class_name is not None:
        raise ValueError(f"Passed ID does not belong to class: {class_name}")
    return int(object_id)
