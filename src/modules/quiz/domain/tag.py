from sqlalchemy import Column, String

from models.base_model import BaseModel


class Tag(BaseModel):
    __tablename__ = "tag"

    name: str = Column(String(500))

    def __str__(self):
        return f"Tag({self.name=})"
