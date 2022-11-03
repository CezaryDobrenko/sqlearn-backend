from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Quiz(BaseModel):
    __tablename__ = "quiz"

    title: str = Column(String(500))
    description: str = Column(String(2000))

    quiz_template_id: int = Column(
        Integer(),
        ForeignKey("quiz_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    quiz_template = relationship("QuizTemplate")

    course_id: int = Column(
        Integer(),
        ForeignKey("course.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    course = relationship("Course", foreign_keys=[course_id], back_populates="quizes")

    assignments: list = relationship("Assignment", lazy="dynamic", uselist=True)

    def __str__(self):
        return f"Quiz({self.title=})"


class QuizTemplate(BaseModel):
    __tablename__ = "quiz_template"

    title: str = Column(String(500))
    description: str = Column(String(2000))

    course_template_id: int = Column(
        Integer(),
        ForeignKey("course_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    course_template = relationship(
        "CourseTemplate",
        foreign_keys=[course_template_id],
        back_populates="quiz_templates",
    )

    assignments_templates: list = relationship(
        "AssignmentTemplate", lazy="dynamic", uselist=True
    )

    def __str__(self):
        return f"QuizTemplate({self.title=})"
