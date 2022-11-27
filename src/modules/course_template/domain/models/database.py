from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class DatabaseAssignmentTemplate(BaseModel):
    __tablename__ = "database_assignment_template"

    name: str = Column(String(500))

    assignment_template_id: int = Column(
        Integer(),
        ForeignKey("assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=True,
    )
    assignment_template = relationship(
        "AssignmentTemplate",
        foreign_keys=[assignment_template_id],
        back_populates="database",
    )

    tables: list = relationship(
        "TableAssignmentTemplate",
        lazy="dynamic",
        uselist=True,
        passive_deletes=True,
    )

    def __str__(self):
        return f"DatabaseAssignmentTemplate({self.name=})"

    __repr__ = __str__
