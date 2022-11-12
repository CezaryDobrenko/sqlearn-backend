from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Course(BaseModel):
    __tablename__ = "course"

    name: str = Column(String(500))
    description: str = Column(String(2000))
    is_finished: bool = Column(Boolean, default=False)

    course_template_id: int = Column(
        Integer(),
        ForeignKey("course_template.id", ondelete="SET NULL"),
        index=True,
        nullable=False,
    )
    course_template = relationship("CourseTemplate")

    user_id: int = Column(
        Integer(),
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    user = relationship("User", foreign_keys=[user_id], back_populates="courses")

    quizes: list = relationship("Quiz", lazy="dynamic", uselist=True)

    def __str__(self):
        return f"Course({self.name=}, {self.user=})"

    __repr__ = __str__
