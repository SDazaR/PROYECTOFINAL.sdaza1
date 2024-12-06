from models.parlor import Parlor
from models.ingredient import Ingredient
from models.product import Product
from models.enums.ingredient_type import IngredientType
from models.enums.product_type import ProductType

# Test objects

base1 = Ingredient(price=2000.0, calories_per_portion=150, name="Base Vainilla", count=10.0, veg=True, type=IngredientType.BASE)
base2 = Ingredient(price=1800.0, calories_per_portion=120, name="Base Chocolate", count=12.0, veg=True, type=IngredientType.BASE)
base3 = Ingredient(price=2200.0, calories_per_portion=170, name="Base Fresa", count=8.0, veg=True, type=IngredientType.BASE)

comp1 = Ingredient(price=500.0, calories_per_portion=50, name="Sirope de Caramelo", count=20.0, veg=True, type=IngredientType.COMPLEMENT)
comp2 = Ingredient(price=600.0, calories_per_portion=30, name="Chispas de Chocolate", count=15.0, veg=True, type=IngredientType.COMPLEMENT)
comp3 = Ingredient(price=400.0, calories_per_portion=40, name="Crema de Nata", count=18.0, veg=False, type=IngredientType.COMPLEMENT)

cup1 = Product(name="Copa Vainilla", sale_price=8000.0, ingredients=[base1, comp1, comp2], type=ProductType.CUP)
milk_shake1 = Product(name="Malteada de Chocolate", sale_price=10000.0, ingredients=[base2, comp2, comp3], type=ProductType.MILKSHAKE)
cup2 = Product(name="Copa Fresa", sale_price=9000.0, ingredients=[base3, comp1, comp2], type=ProductType.CUP)
milk_shake2 = Product(name="Malteada de Fresa", sale_price=11000.0, ingredients=[base3, comp2, comp3], type=ProductType.MILKSHAKE)

parlor = Parlor(name="Helato", products=[cup1, milk_shake1, cup2, milk_shake2])


def fill_db(app,db):
    with app.app_context():
        db.session.add(parlor)
        db.session.commit()
