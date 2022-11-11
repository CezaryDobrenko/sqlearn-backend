from instance_access import has_user_access
from modules.user.domain.models.user import User


@has_user_access.register(User)
def _has_user_access_other_user(instance: User, user: User) -> bool:
    return instance == user
