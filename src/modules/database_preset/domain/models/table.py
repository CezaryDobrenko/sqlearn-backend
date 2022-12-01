from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Table(BaseModel):
    __tablename__ = "table"

    name: str = Column(String(500))
    description: str = Column(String(2000))

    database_id: int = Column(
        Integer(),
        ForeignKey("database.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    database = relationship(
        "Database", foreign_keys=[database_id], back_populates="tables"
    )

    columns: list = relationship(
        "TableColumn", lazy="dynamic", uselist=True, passive_deletes=True
    )
    relations: list = relationship(
        "TableRelation",
        lazy="dynamic",
        uselist=True,
        primaryjoin="Table.id == TableRelation.table_id",
        passive_deletes=True,
    )
    related_by: list = relationship(
        "TableRelation",
        lazy="dynamic",
        uselist=True,
        primaryjoin="Table.id == TableRelation.relation_table_id",
        passive_deletes=True,
    )

    def __str__(self):
        return f"Table({self.name=})"

    __repr__ = __str__

    def has_column(self, column_name: str) -> bool:
        for column in self.columns:
            if column.name == column_name:
                return True
        return False
