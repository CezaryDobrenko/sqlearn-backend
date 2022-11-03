from sqlalchemy import Column, String

from models.base_model import BaseModel
from models.utils import generate_hash


class User(BaseModel):
    email: str = Column(String(255), index=True, unique=True)
    password: str = Column(String(255))

    def change_email(self, email: str) -> None:
        self.email = email

    def set_password(self, raw_password: str) -> None:
        password = generate_hash(raw_password)
        self.password = password

    def __str__(self):
        return f"User(email={self.email})"
