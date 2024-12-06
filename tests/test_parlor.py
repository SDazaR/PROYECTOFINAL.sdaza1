from unittest import TestCase
from models.ingredient import Ingredient
from models.product import Product
from models.parlor import Parlor
from models.enums.ingredient_type import IngredientType
from app import app
from models.enums.product_type import ProductType
from utils.functions import count_calories, costs, best_product

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


class TestParlor(TestCase):
    
    def setUp(self) -> None:
        self.client = app.test_client()

    def tearDown(self) -> None:
        pass

    def test_healthy_ingredient(self):
        for ingredient in parlor.ingredients:
            self.assertEqual(ingredient.is_healthy(), True)
    
    def test_replenish_ingredient(self):
        for ingredient in parlor.ingredients:
            previoust_count = ingredient.count
            ingredient.replenish()

            if ingredient.type.value == IngredientType.BASE.value:
                self.assertEqual(ingredient.count, previoust_count+5)
            elif ingredient.type.value == IngredientType.COMPLEMENT.value:
                self.assertEqual(ingredient.count, previoust_count+10)
            

    def test_reset_count(self):
        for ingredient in parlor.ingredients:
            ingredient.reset_count()
            self.assertEqual(ingredient.count, 0)


    def test_count_calories(self):
        for product in parlor.products:
            if product.type.value == ProductType.CUP.value:
                response = count_calories([ingredient.calories_per_portion for ingredient in product.ingredients])
            elif product.type.value == ProductType.MILKSHAKE.value:
                response = round(count_calories([ingredient.calories_per_portion for ingredient in product.ingredients])/0.95 + 200, 2)
            self.assertEqual(product.count_calories(), response)

    def test_costs(self):
        for product in parlor.products:
            if product.type.value == ProductType.CUP.value:
                response = costs([ingredient.__dict__ for ingredient in product.ingredients])
            elif product.type.value == ProductType.MILKSHAKE.value:
                response = costs([ingredient.__dict__ for ingredient in product.ingredients]) + 500
            self.assertEqual(product.costs(), response)

    def test_profiability(self):
        for product in parlor.products:
            response = product.sale_price - product.costs()
            self.assertEqual(product.profitability(), response)

    def test_find_best(self):
        product_list = []
        for product in parlor.products:
            product_list.append({"name": product.name, "profitability": product.profitability()})
        response = best_product(product_list)
        self.assertEqual(parlor.best_product(), response)

    def test_make_sale(self):
        response = self.client.get("/parlor/1/makeSale/Copa%20Vainilla")
        self.assertEqual(response.status_code, 200)