from db.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, Boolean, Enum, ForeignKey
from models.enums.ingredient_type import IngredientType
from flask_login import UserMixin
from marshmallow import Schema, fields
from models.parlor import Parlor


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False)
    password: Mapped[str] = mapped_column(String(40), nullable=False)
    parlor_id: Mapped[int] = mapped_column(ForeignKey("parlor.id"), nullable=False)
    parlor: Mapped["Parlor"] = relationship("Parlor", lazy="joined")

    @classmethod
    def credentials_exist (cls, username: str, password: str, parlor_id: int)-> bool:
        user = cls.query.filter_by(username=username, password=password, parlor_id=parlor_id).first()
        return user
        


class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str()
    email = fields.Email()