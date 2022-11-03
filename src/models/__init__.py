from sqlalchemy.orm import configure_mappers

from modules.quiz.domain import *  # noqa
from modules.user.domain import *  # noqa

configure_mappers()
