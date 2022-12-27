from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Session, relationship

from models.base_model import BaseModel
from modules.course_template.domain.services.row_action_service import RowActionService
from modules.database_preset.domain.models.relation import RelationAction


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

    def delete(self, session: Session) -> bool:
        service = RowActionService(session, on_delete=True)
        service.execute_on_delete(self)
        session.delete(self)
        return True

    def update(self, session: Session, **update) -> bool:
        raise Exception("Not implemented")
