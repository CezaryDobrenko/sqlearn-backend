from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate


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
        "TableColumnAssignmentTemplate",
        lazy="dynamic",
        uselist=True,
        passive_deletes=True,
    )
    relations: list = relationship(
        "TableRelationAssignmentTemplate",
        lazy="dynamic",
        uselist=True,
        primaryjoin="TableAssignmentTemplate.id == TableRelationAssignmentTemplate.table_id",
        passive_deletes=True,
    )
    related_by: list = relationship(
        "TableRelationAssignmentTemplate",
        lazy="dynamic",
        uselist=True,
        primaryjoin="TableAssignmentTemplate.id == TableRelationAssignmentTemplate.relation_table_id",
        passive_deletes=True,
    )

    def __str__(self):
        return f"TableAssignmentTemplate({self.name=})"

    __repr__ = __str__

    def get_column(self, column_name: str) -> Optional[TableColumnAssignmentTemplate]:
        if self.has_column(column_name):
            return self.columns.filter(
                TableColumnAssignmentTemplate.name == column_name
            ).first()
        return None

    def has_column(self, column_name: str) -> bool:
        for column in self.columns:
            if column.name == column_name:
                return True
        return False

    def has_autoincrement_defined(self):
        for column in self.columns:
            if column.is_autoincrement:
                return column
        return None
