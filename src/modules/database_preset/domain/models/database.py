from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Database(BaseModel):
    __tablename__ = "database"

    name: str = Column(String(500))

    user_id: int = Column(
        Integer(),
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    user = relationship("User", foreign_keys=[user_id], back_populates="databases")

    tables: list = relationship(
        "Table", lazy="dynamic", uselist=True, passive_deletes=True
    )

    def __str__(self):
        return f"Database({self.name=})"

    __repr__ = __str__
