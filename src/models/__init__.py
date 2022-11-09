from sqlalchemy.orm import configure_mappers

from modules.quiz.domain.models import *  # noqa
from modules.user.domain.models import *  # noqa

configure_mappers()
