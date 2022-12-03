import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class ColumnType(enum.Enum):
    INTEGER = "INTEGER"
    NUMERIC = "NUMERIC"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"


COLUMN_TYPE = Enum(ColumnType)
RELEVANT_FIELDS = ["name", "type"]


class TableColumn(BaseModel):
    __tablename__ = "table_column"

    name: str = Column(String(500))
    type: str = Column(COLUMN_TYPE, nullable=False)
    length: int = Column(Integer)
    is_null: bool = Column(Boolean)
    is_unique: bool = Column(Boolean)

    table_id: int = Column(
        Integer(),
        ForeignKey("table.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    table = relationship("Table", foreign_keys=[table_id], back_populates="columns")

    def __str__(self):
        return f"TableColumn({self.name=} {self.type=} {self.length=})"

    __repr__ = __str__

    @property
    def assigned_table_id(self):
        return self.table_id

    def is_relevant_field_updated(self, **kwargs) -> bool:
        for field in RELEVANT_FIELDS:
            if field in kwargs:
                if getattr(self, field) != kwargs[field]:
                    return True
        return False
