from models.product import Product
from utils.functions import best_product
from models.enums.ingredient_type import IngredientType
from models.enums.product_type import ProductType
from models.ingredient import Ingredient
from db.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from typing import List


parlor_product_association = db.Table(
    "parlor_product",
    Column("parlor_id", Integer, ForeignKey("parlor.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("product.id"), primary_key=True)
)

parlor_ingredient_association = db.Table(
    "parlor_ingredient",
    Column("parlor_id", Integer, ForeignKey("parlor.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True),
)

class Parlor(db.Model):

    __tablename__ = "parlor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    daily_sales: Mapped[int] = mapped_column(nullable=False)
    products: Mapped[List[Product]] = relationship(
        Product,
        secondary=parlor_product_association,
        lazy="select"
    )
    ingredients: Mapped[List[Ingredient]] = relationship(
        Ingredient,
        secondary=parlor_ingredient_association,
        lazy="select"
    )

    # Constructor


    def __init__(self, name: str, products: list["Product"]) -> None:
        if len(products) > 4:
            raise ValueError("Un establecimiento puede tener como máximo 4 productos.")
        super().__init__(name=name, products=products, daily_sales=0)
        self.ingredients = []
        for product in self.products:
            for ingredient in product.ingredients:
                if ingredient not in self.ingredients:
                    self.ingredients.append(ingredient)

    # Métodos

    def best_product(self) -> str:
        product_list = []
        for product in self.products:
            product_list.append({"name": product.name, "profitability": product.profitability()})
        return best_product(product_list)
    
    def make_sale(self, product_name: str) -> bool:
        if not any(product_name == product.name for product in self.products):
            raise ValueError("El valor debe ser el nombre de un producto en " + self.name + ".")
        products = [product for product in self.products if product.name == product_name]

        if len(products) > 1:
            raise ValueError("Hay múltiples productos con ese nombre.")

        product = products[0]

        for ingredient in product.ingredients:
            if ingredient.type.name == IngredientType.BASE.name and ingredient.count < 0.2:
                raise ValueError("¡Oh no! Nos hemos quedado sin " + ingredient.name + ".")
            if ingredient.type.name == IngredientType.COMPLEMENT.name and ingredient.count < 1:
                raise ValueError("¡Oh no! Nos hemos quedado sin " + ingredient.name + ".")
        new_ingredients = self.ingredients.copy()
        for ingredient in product.ingredients:
            new_ingredient = ingredient.copy()
            if ingredient.type.name == IngredientType.BASE.name:
                new_ingredient.count = ingredient.copy().count - 0.2
            if ingredient.type.name == IngredientType.COMPLEMENT.name:
                new_ingredient.count = ingredient.copy().count - 1
            for parlor_ingredient in new_ingredients:
                if parlor_ingredient.id == new_ingredient.id:
                    new_ingredients.remove(parlor_ingredient)
                    new_ingredients.append(new_ingredient)
                    break
        self.daily_sales += 1
        self.ingredients = new_ingredients.copy()

        return "Vendido"
