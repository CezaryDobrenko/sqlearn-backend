from sqlalchemy.orm import configure_mappers

from modules.course.domain.models import *  # noqa
from modules.course_template.domain.models import *  # noqa
from modules.database_preset.domain.models import *  # noqa
from modules.user.domain.models import *  # noqa

configure_mappers()
