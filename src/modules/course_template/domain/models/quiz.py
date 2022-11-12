from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


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

    __repr__ = __str__

    def update(self, **kwargs):
        super().update(**kwargs)
        self.course_template.withdraw()
