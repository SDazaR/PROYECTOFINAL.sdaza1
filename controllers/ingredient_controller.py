from flask import jsonify, Blueprint, render_template
from models.parlor import parlor_product_association, parlor_ingredient_association
from models.ingredient import Ingredient, IngredientSchema
from db.db import db

ingredient_blueprint = Blueprint('ingredient_bp', __name__, url_prefix="/ingredient")

@ingredient_blueprint.route("/", methods=["GET"])
def get_ingredients():
    try:
        ingredients = Ingredient.query.all()
        ingredients_schema = IngredientSchema(many=True)
        return jsonify({"ingredients": ingredients_schema.dump(ingredients)}) 
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener la lista de ingredientes. Causa: " + str(e)}
    

@ingredient_blueprint.route("/<int:ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id: int):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        ingredient_schema = IngredientSchema(many=False)
        return jsonify({"ingredient": ingredient_schema.dump(ingredient)}) 
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener el ingrediente. Causa: " + str(e)}


@ingredient_blueprint.route("/name/<string:name>", methods=["GET"])
def get_ingredient_by_name(name: str):
    try:
        ingredient = Ingredient.query.filter(Ingredient.name.ilike(f"%{name}%")).first()
        if not ingredient:
            return jsonify({"success": False, "message": "No se encontró un ingrediente con ese nombre"}), 404
        ingredient_schema = IngredientSchema(many=False)
        return jsonify({"ingredient": ingredient_schema.dump(ingredient)})
    except Exception as e:
        return {"success": False, "message": "No fue posible obtener el ingrediente. Causa: " + str(e)}, 500


@ingredient_blueprint.route("/<int:ingredient_id>/is_healthy", methods=["GET"])
def is_ingredient_healthy(ingredient_id: int):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return jsonify({"success": False, "message": "No se encontró un ingrediente con ese ID"}), 404
        is_healthy = ingredient.is_healthy()
        return jsonify({"is_healthy": is_healthy})
    except Exception as e:
        return {"success": False, "message": "No fue posible verificar si el ingrediente es sano. Causa: " + str(e)}, 500


@ingredient_blueprint.route("/<int:ingredient_id>/replenish", methods=["PUT"])
def replenish_ingredient(ingredient_id: int):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return jsonify({"success": False, "message": "No se encontró un ingrediente con ese ID"}), 404
        ingredient.replenish()
        db.session.commit()
        return jsonify({"success": True, "message": "Ingrediente reabastecido correctamente", "new_count": ingredient.count})
    except Exception as e:
        return {"success": False, "message": "No fue posible reabastecer el ingrediente. Causa: " + str(e)}, 500


@ingredient_blueprint.route("/<int:ingredient_id>/reset", methods=["PUT"])
def reset_ingredient_count(ingredient_id: int):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return jsonify({"success": False, "message": "No se encontró un ingrediente con ese ID"}), 404
        ingredient.reset_count()
        db.session.commit()
        return jsonify({"success": True, "message": "El inventario del ingrediente se ha renovado correctamente", "new_count": ingredient.count})
    except Exception as e:
        return {"success": False, "message": "No fue posible renovar el inventario del ingrediente. Causa: " + str(e)}, 500
