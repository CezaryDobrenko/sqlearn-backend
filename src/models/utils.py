import hashlib
from contextlib import contextmanager
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Query, Session

from config import SALT

from .base_model import BaseModel


def string_to_date_converter(raw_date: str, format: str = "%d-%m-%Y") -> datetime:
    return datetime.strptime(raw_date, format)


def date_to_string_converter(
    date: Optional[datetime], format: str = "%d-%m-%Y"
) -> Optional[str]:
    if date:
        return date.strftime(format)
    return None


def is_model_joined(query: Query, model: BaseModel) -> bool:
    if hasattr(query, "_compile_state"):  # SQLAlchemy >= 1.4
        join_entities = query._compile_state()._join_entities  # type: ignore
    else:
        join_entities = query._join_entities  # type: ignore
    if model in [mapper.class_ for mapper in join_entities]:
        return True
    return False


def generate_hash(raw_password: str) -> str:
    hash = hashlib.pbkdf2_hmac("sha256", raw_password.encode("utf-8"), SALT, 100000)
    return hashlib.sha256(hash).hexdigest()


def get_or_create(session: Session, model: BaseModel, **kwargs) -> tuple[object, bool]:
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance, True


@contextmanager
def transaction_scope(session: Session) -> None:
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
