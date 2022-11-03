import re
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, MetaData, create_engine, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from config import Config

GlobalId = str
first_cap_re = re.compile("(.)([A-Z][a-z]+)")
all_cap_re = re.compile("([a-z0-9])([A-Z])")


def camel_case_to_underscore(text: str) -> str:
    s1 = first_cap_re.sub(r"\1_\2", text)
    return all_cap_re.sub(r"\1_\2", s1).lower()


class Base:
    @declared_attr
    def __tablename__(cls):
        return camel_case_to_underscore(cls.__name__)

    id: int = Column(Integer, primary_key=True, autoincrement=True)


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
metadata = MetaData(bind=engine)
AbstractModel = declarative_base(cls=Base)


class BaseModel(AbstractModel):
    __abstract__ = True

    modified = Column(
        DateTime,
        server_default=func.timezone("UTC", func.now()),
        onupdate=datetime.utcnow,
    )
    created = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.timezone("UTC", func.now()),
    )

    def update(self, **kwargs):
        self._update(**kwargs)

    def _update(self, **kwargs):
        for field_name, value in kwargs.items():
            self.update_attribute(field_name, value)

    def update_attribute(self, field_name, value):
        if hasattr(self, field_name):
            if isinstance(value, str):
                setattr(self, field_name, value.strip())
            else:
                setattr(self, field_name, value)
