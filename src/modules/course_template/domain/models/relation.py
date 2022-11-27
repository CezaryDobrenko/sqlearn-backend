from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel
from modules.database_preset.domain.models.relation import RELATION_ACTION


class TableRelationAssignmentTemplate(BaseModel):
    __tablename__ = "table_relation_assignment_template"

    name: str = Column(String(500))
    action: str = Column(RELATION_ACTION, nullable=False)

    relation_column_name: str = Column(String(500))
    relation_table_id: int = Column(
        Integer(),
        ForeignKey("table_assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    relation_table = relationship(
        "TableAssignmentTemplate",
        foreign_keys=[relation_table_id],
        back_populates="related_by",
    )

    table_column_name: str = Column(String(500))
    table_id: int = Column(
        Integer(),
        ForeignKey("table_assignment_template.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    table = relationship(
        "TableAssignmentTemplate",
        foreign_keys=[table_id],
        back_populates="relations",
    )

    def __str__(self):
        return f"TableRelationAssignmentTemplate({self.name=} from={self.table}, to={self.relation_table})"

    __repr__ = __str__
