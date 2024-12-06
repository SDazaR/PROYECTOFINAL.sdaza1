from flask import jsonify, Blueprint, render_template
from models.product import Product, ProductSchema
from models.parlor import Parlor, parlor_product_association, parlor_ingredient_association
from models.ingredient import Ingredient, IngredientSchema
from db.db import db

product_blueprint = Blueprint('product_bp', __name__, url_prefix="/product")


@product_blueprint.route("/", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        products_schema = ProductSchema(many=True)
        return jsonify({"products": products_schema.dump(products)}) 
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener la lista de productos. Causa: " + str(e)}
    

@product_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    try:
        product = Product.query.get(product_id)
        product_schema = ProductSchema(many=False)
        return jsonify({"products": product_schema.dump(product)}) 
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener el producto. Causa: " + str(e)}


@product_blueprint.route("/name/<string:name>", methods=["GET"])
def get_product_by_name(name: str):
    try:
        product = Product.query.filter_by(name=name).first()
        if not product:
            return {"success": False, "message": "Producto no encontrado"}
        product_schema = ProductSchema(many=False)
        return jsonify({"product": product_schema.dump(product)})
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener el producto. Causa: " + str(e)}


@product_blueprint.route("/<int:product_id>/calories", methods=["GET"])
def get_product_calories(product_id: int):
    try:
        product = Product.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}
        calories = product.count_calories()
        return jsonify({"calories": calories})
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener las calorías del producto. Causa: " + str(e)}


@product_blueprint.route("/<int:product_id>/profitability", methods=["GET"])
def get_product_profitability(product_id: int):
    try:
        product = Product.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}
        profitability = product.profitability()
        return jsonify({"profitability": profitability})
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener la rentabilidad del producto. Causa: " + str(e)}


@product_blueprint.route("/<int:product_id>/cost", methods=["GET"])
def get_product_cost(product_id: int):
    try:
        product = Product.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}
        cost = product.costs()
        return jsonify({"cost": cost})
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener el costo del producto. Causa: " + str(e)} 

