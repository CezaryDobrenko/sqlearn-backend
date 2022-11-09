import inspect
from functools import singledispatch, wraps
from typing import Any

from models import User
from models.base_model import BaseModel


def _get_instance_pk(args: tuple, args_names: list[str], model: BaseModel) -> int:
    args_names = [name for name in args_names if name != "self"]
    pk_keyword = f"{model.__tablename__}_id"
    args_index = args_names.index(pk_keyword)
    instance_pk = args[args_index]
    return instance_pk


def authorize_access(model: BaseModel, **extra_args):
    def decorator(func):
        @wraps(func)
        def wrapper(root, *args, **kwargs):
            if user := kwargs.get("current_user"):
                args_names = inspect.getfullargspec(func).args
                instance_pk = _get_instance_pk(args, args_names, model)
                if instance := root.session.query(model).get(instance_pk):
                    if has_user_access(instance, user):
                        return func(root, *args, **kwargs)
                    raise Exception("Permision Denied")
                raise Exception("Instance does not exist")
            raise Exception("Unauthenticated User")

        return wrapper

    return decorator


@singledispatch
def has_user_access(instance: Any, user: User) -> None:
    raise NotImplementedError


import modules.quiz.domain.services.authorize  # noqa
