from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel
from modules.database_preset.domain.models.column import COLUMN_TYPE, RELEVANT_FIELDS


class TableColumnAssignmentTemplate(BaseModel):
    __tablename__ = "table_column_assignment_template"

    name: str = Column(String(500))
    type: str = Column(COLUMN_TYPE, nullable=False)
    length: int = Column(Integer)
    is_null: bool = Column(Boolean)
    is_unique: bool = Column(Boolean)

    table_assignment_template_id: int = Column(
        Integer(),
        ForeignKey("table_assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    table_assignment_template = relationship(
        "TableAssignmentTemplate",
        foreign_keys=[table_assignment_template_id],
        back_populates="columns",
    )
    data: list = relationship(
        "TableColumnDataTemplate", lazy="dynamic", uselist=True, passive_deletes=True
    )

    def __str__(self):
        return f"TableColumn({self.name=} {self.type=} {self.length=})"

    __repr__ = __str__

    @property
    def assigned_table_id(self):
        return self.table_assignment_template_id

    def is_relevant_field_updated(self, **kwargs) -> bool:
        for field in RELEVANT_FIELDS:
            if field in kwargs:
                if getattr(self, field) != kwargs[field]:
                    return True
        return False
