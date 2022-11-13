from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel
from models.utils import generate_hash


class User(BaseModel):
    email: str = Column(String(255), index=True, unique=True)
    password: str = Column(String(255))

    courses: list = relationship("Course", lazy="dynamic", uselist=True)
    databases: list = relationship("Database", lazy="dynamic", uselist=True)
    course_templates: list = relationship(
        "CourseTemplate", lazy="dynamic", uselist=True
    )

    def change_email(self, email: str) -> None:
        self.email = email

    def set_password(self, raw_password: str) -> None:
        password = generate_hash(raw_password)
        self.password = password

    def check_password(self, raw_password: str) -> bool:
        if self.password == generate_hash(raw_password):
            return True
        return False

    def __str__(self):
        return f"User(email={self.email})"

    __repr__ = __str__
