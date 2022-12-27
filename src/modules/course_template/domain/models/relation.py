from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
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

    @property
    def source_column(self) -> TableColumnAssignmentTemplate:
        return self.table.columns.filter(
            TableColumnAssignmentTemplate.name == self.table_column_name
        ).first()

    @property
    def relation_column(self) -> TableColumnAssignmentTemplate:
        return self.relation_table.columns.filter(
            TableColumnAssignmentTemplate.name == self.relation_column_name
        ).first()
