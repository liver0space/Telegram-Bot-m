from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from . import db


class Admin(db.Model):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'<Admin {self.id} {self.username} {self.password}>'


class User(db.Model):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    def __repr__(self) -> str:
        return f'<User {self.user_id}>'
