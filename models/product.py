from utils.functions import profitability
from models.ingredient import Ingredient
from db.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, Boolean, Table, Column, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from models.enums.product_type import ProductType
from utils.functions import costs, count_calories
from marshmallow import Schema, fields



product_ingredient_association = db.Table(
    "product_ingredient",
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("product.id"), primary_key=True),
)

class Product(db.Model):

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    sale_price: Mapped[float] = mapped_column(Float, nullable=False)
    ingredients: Mapped[List[Ingredient]] = relationship(
        Ingredient,
        secondary=product_ingredient_association,
        lazy="select"
    )
    type: Mapped[ProductType] = mapped_column(Enum(ProductType), nullable=False)

    # Constructor

    def __init__(self, name: str, sale_price: float, ingredients: list[Ingredient], type: ProductType):
        if len(ingredients) > 3:
            raise ValueError("A product can have at most 4 ingredients.")
        super().__init__(name=name, ingredients=ingredients, sale_price=sale_price, type=type)

    # Methods
    def count_calories(self) -> float:
        if self.type == ProductType.CUP:
            return count_calories([ingredient.calories_per_portion for ingredient in self.ingredients])
        elif self.type == ProductType.MILKSHAKE:
            return round(count_calories([ingredient.calories_per_portion for ingredient in self.ingredients])/0.95 + 200, 2)
    
    def costs(self) -> float:
        if self.type == ProductType.CUP:
            return costs([ingredient.__dict__ for ingredient in self.ingredients])
        elif self.type == ProductType.MILKSHAKE:
            return costs([ingredient.__dict__ for ingredient in self.ingredients]) + 500
       
    def profitability(self) -> float:
        return self.sale_price - self.costs()


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    sale_price = fields.Float(required=True)
    ingredients = fields.List(fields.Nested("IngredientSchema"), required=True)
    type = fields.Str(required=True)
