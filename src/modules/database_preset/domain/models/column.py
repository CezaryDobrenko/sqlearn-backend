import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class ColumnType(enum.Enum):
    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"
    NULL = "NULL"


class TableColumn(BaseModel):
    __tablename__ = "table_column"

    name: str = Column(String(500))
    type: str = Column(Enum(ColumnType), nullable=False)
    length: int = Column(Integer)
    is_null: bool = Column(Boolean)

    table_id: int = Column(
        Integer(),
        ForeignKey("table.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    table = relationship("Table", foreign_keys=[table_id], back_populates="columns")

    def __str__(self):
        return f"TableColumn({self.name=} {self.type=} {self.length=} {self.is_null=})"

    __repr__ = __str__
