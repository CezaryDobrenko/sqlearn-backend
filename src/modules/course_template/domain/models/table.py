from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class TableAssignmentTemplate(BaseModel):
    __tablename__ = "table_assignment_template"

    name: str = Column(String(500))
    description: str = Column(String(2000))

    database_assignment_template_id: int = Column(
        Integer(),
        ForeignKey("database_assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    database_assignment_template = relationship(
        "DatabaseAssignmentTemplate",
        foreign_keys=[database_assignment_template_id],
        back_populates="tables",
    )

    columns: list = relationship(
        "TableColumnAssignmentTemplate", lazy="dynamic", uselist=True
    )
    relations: list = relationship(
        "TableRelationAssignmentTemplate",
        lazy="dynamic",
        uselist=True,
        primaryjoin="TableAssignmentTemplate.id == TableRelationAssignmentTemplate.table_id",
        passive_deletes=True,
    )

    def __str__(self):
        return f"TableAssignmentTemplate({self.name=})"

    __repr__ = __str__
