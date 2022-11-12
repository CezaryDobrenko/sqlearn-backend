from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class QueryHistory(BaseModel):
    __tablename__ = "query_history"

    query: str = Column(String)
    is_valid: bool = Column(Boolean)

    assignment_id: int = Column(
        Integer(),
        ForeignKey("assignment.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    assignment = relationship(
        "Assignment", foreign_keys=[assignment_id], back_populates="queries"
    )

    def __str__(self):
        return f"QueryHistory({self.query=}, {self.assignment=})"

    __repr__ = __str__
