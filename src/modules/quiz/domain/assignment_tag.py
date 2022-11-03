from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class AssignmentTag(BaseModel):
    __tablename__ = "assignment_tag"

    tag_id: int = Column(
        Integer(),
        ForeignKey("tag.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    tag = relationship("Tag")

    assignment_id: int = Column(
        Integer(),
        ForeignKey("assignment.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    assignment = relationship(
        "Assignment", foreign_keys=[assignment_id], back_populates="tags"
    )

    def __str__(self):
        return f"AssignmentTag({self.assignment=}, {self.tag=})"

    __repr__ = __str__


class AssignmentTemplateTag(BaseModel):
    __tablename__ = "assignment_template_tag"

    tag_id: int = Column(
        Integer(),
        ForeignKey("tag.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    tag = relationship("Tag")

    assignment_template_id: int = Column(
        Integer(),
        ForeignKey("assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    assignment_template = relationship(
        "AssignmentTemplate",
        foreign_keys=[assignment_template_id],
        back_populates="template_tags",
    )

    def __str__(self):
        return f"AssignmentTemplateTag({self.assignment_template=}, {self.tag=})"

    __repr__ = __str__
