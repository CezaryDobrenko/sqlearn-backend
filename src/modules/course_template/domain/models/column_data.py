from typing import Optional

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

    table_row_assignment_template_id: int = Column(
        Integer(),
        ForeignKey("table_row_assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    table_row_assignment_template = relationship(
        "TableRowAssignmentTemplate",
        foreign_keys=[table_row_assignment_template_id],
        back_populates="cells",
    )

    def __str__(self):
        return f"TableColumnDataTemplate({self.value=})"

    __repr__ = __str__

    def set_value(self, value: Optional[str] = None) -> None:
        column = self.table_column_assignment_template
        table = column.table_assignment_template

        if value and column.is_autoincrement:
            # TODO: check if id value is not taken by other row
            self.value = value
            table.set_autoincrement_index(int(value))
            return None

        if value:
            self.value = value
            return None

        if column.is_autoincrement:
            self.value = table.get_autoincrement_index()
            table.update_autoincrement_index()
            return None

        self.value = column.get_default_value
