from flask import jsonify, Blueprint, render_template
from flask_login import login_required, current_user

from models.parlor import Parlor, parlor_product_association, parlor_ingredient_association
from models.ingredient import Ingredient
from models.product import Product
from db.db import db

parlor_blueprint = Blueprint('parlor_bp', __name__, url_prefix="/parlor")

@parlor_blueprint.route("/<int:id>")
@login_required
def index(id:int):
    parlor = Parlor.query.get(id)
    return render_template("index.html", menu=parlor.products, parlor_name=parlor.name, iden=id)


@parlor_blueprint.route("/<int:id>/bestProduct")
@login_required
def best_product_handler(id:int):
    try:
        parlor = Parlor.query.get(id)
    except:
        return "No existe una heladería con ese id"
    resp = parlor.best_product()
    return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)


@parlor_blueprint.route("/<int:id>/makeSale/<product>")
@login_required
def make_sale_handler(product:str, id:int):
    try:
        parlor = Parlor.query.get(id)
        if not parlor:
            return "No existe una heladería con ese id"
    except:
        resp = "No existe una heladería con ese id"
        return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)
    try:
        response = parlor.make_sale(product)  
    except ValueError as e:
        resp = str(e)
        return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)
    try:
        for ingredient in parlor.ingredients.copy():
            db_ingredient = Ingredient.query.get(ingredient.id)
            db.session.delete(db_ingredient)
            db.session.add(ingredient)
        db.session.commit()
    except Exception as e:
        resp =  "No se pudo actualizar los valores de la heladería. Causa:" + str(e)
        return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)

    resp = response

    return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)


@parlor_blueprint.route("/<int:id>/makeSale/<string:product_id>", methods=["PUT"])
def sell_product_handler(id: int, product_id: str):
    try:
        parlor = Parlor.query.get(id)
        if not parlor:
            return jsonify({"success": False, "message": "No existe una heladería con ese ID"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "Error al buscar la heladería. Causa: " + str(e)}), 500

    try:
        product = Product.query.get(product_id)
        response = parlor.make_sale(product.name)
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    try:
        for ingredient in parlor.ingredients.copy():
            db_ingredient = Ingredient.query.get(ingredient.id)
            if db_ingredient:
                db.session.delete(db_ingredient)
                db.session.add(ingredient)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "No se pudo actualizar los valores de la heladería. Causa: " + str(e)
        }), 500

    return jsonify({
        "success": True,
        "message": response,
        "parlor_id": id,
        "product_name": product.name
    }), 200