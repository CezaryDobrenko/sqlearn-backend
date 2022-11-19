from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class TableColumnDataTemplate(BaseModel):
    __tablename__ = "table_column_data_template"

    value: str = Column(String(500))

    table_column_assignment_template_id: int = Column(
        Integer(),
        ForeignKey("table_column_assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    table_column_assignment_template = relationship(
        "TableColumnAssignmentTemplate",
        foreign_keys=[table_column_assignment_template_id],
        back_populates="data",
    )

    def __str__(self):
        return f"TableColumnDataTemplate({self.value=})"

    __repr__ = __str__
