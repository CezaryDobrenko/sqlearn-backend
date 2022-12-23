from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class TableRowAssignmentTemplate(BaseModel):
    __tablename__ = "table_row_assignment_template"

    ordinal: int = Column(Integer)

    table_assignment_template_id: int = Column(
        Integer(),
        ForeignKey("table_assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    table_assignment_template = relationship(
        "TableAssignmentTemplate",
        foreign_keys=[table_assignment_template_id],
        back_populates="rows",
    )

    cells: list = relationship(
        "TableColumnDataTemplate", lazy="dynamic", uselist=True, passive_deletes=True
    )

    def __str__(self):
        return f"TableRowAssignmentTemplate({self.ordinal=})"

    __repr__ = __str__
