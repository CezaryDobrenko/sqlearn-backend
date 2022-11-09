from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Assignment(BaseModel):
    __tablename__ = "assignment"

    ordinal: int = Column(Integer)
    title: str = Column(String(500))
    description: str = Column(String(5000))
    solution: str = Column(String)

    assignment_template_id: int = Column(
        Integer(),
        ForeignKey("assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    assignment_template = relationship("AssignmentTemplate")

    quiz_id: int = Column(
        Integer(),
        ForeignKey("quiz.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    quiz = relationship("Quiz", foreign_keys=[quiz_id], back_populates="assignments")

    queries: list = relationship("QueryHistory", lazy="dynamic", uselist=True)
    tags: list = relationship("AssignmentTag", lazy="dynamic", uselist=True)

    def __str__(self):
        return f"Assignment({self.ordinal=}, {self.title=})"

    __repr__ = __str__


class AssignmentTemplate(BaseModel):
    __tablename__ = "assignment_template"

    ordinal: int = Column(Integer)
    title: str = Column(String(500))
    description: str = Column(String(5000))
    owner_solution: str = Column(String)

    quiz_template_id: int = Column(
        Integer(),
        ForeignKey("quiz_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    quiz_template = relationship(
        "QuizTemplate",
        foreign_keys=[quiz_template_id],
        back_populates="assignments_templates",
    )

    template_tags: list = relationship(
        "AssignmentTemplateTag", lazy="dynamic", uselist=True
    )

    def __str__(self):
        return f"QuizTemplate({self.ordinal=}, {self.title=})"

    __repr__ = __str__
