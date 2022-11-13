import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class RelationAction(enum.Enum):
    NO_ACTION = "NO ACTION"
    SET_NULL = "SET NULL"
    SET_DEFAULT = "SET DEFAULT"
    CASCADE = "CASCADE"


class TableRelation(BaseModel):
    __tablename__ = "table_relation"

    name: str = Column(String(500))
    action: str = Column(Enum(RelationAction), nullable=False)

    relation_column_name: str = Column(String(500))
    relation_table_id: int = Column(
        Integer(),
        ForeignKey("table.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    relation_table = relationship("Table", foreign_keys=[relation_table_id])

    table_column_name: str = Column(String(500))
    table_id: int = Column(
        Integer(),
        ForeignKey("table.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    table = relationship("Table", foreign_keys=[table_id], back_populates="relations")

    def __str__(self):
        return (
            f"TableRelation({self.name=} from={self.table}, to={self.relation_table})"
        )

    __repr__ = __str__
