from abc import abstractmethod
from utils.functions import is_healthy
from db.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, Boolean, Enum
from models.enums.ingredient_type import IngredientType
from marshmallow import Schema, fields

class Ingredient(db.Model):

    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    calories_per_portion: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[float] = mapped_column(Float, nullable=False)
    veg: Mapped[bool] = mapped_column(Boolean, nullable=False)
    type: Mapped[IngredientType] = mapped_column(Enum(IngredientType), nullable=False)

    """ # Constructor

    def __init__(self, price: float, calories_per_portion: int, name: str, count: float, veg: bool):
        self.price = price
        self.calories_per_portion = calories_per_portion
        self.name = name
        self.count = count
        self.veg = veg """

    # Methods

    def copy(self):
            return Ingredient(id=self.id, 
                              name=self.name, 
                              price=self.price, 
                              calories_per_portion=self.calories_per_portion, 
                              count=self.count, 
                              type=self.type,
                              veg=self.veg)  # Adaptado a los atributos de tu clase

    def is_healthy(self) -> bool:
        return is_healthy(self.calories_per_portion, self.veg)

    def replenish(self) -> None:
        if self.type == IngredientType.BASE:
            self.count += 5
        elif self.type == IngredientType.COMPLEMENT:
            self.count += 10

    def reset_count(self) -> None:
        self.count = 0.0


class IngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    calories_per_portion = fields.Int(required=True)
    count = fields.Float(required=True)
    veg = fields.Bool(required=True)
    type = fields.Str(required=True)