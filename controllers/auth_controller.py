from flask import jsonify, Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from db.db import db
from models.users import User
from models.parlor import Parlor


auth_blueprint = Blueprint('auth_bp', __name__, url_prefix="/auth")

@auth_blueprint.route("/parlor/<int:id>/login", methods=["POST"])
def login(id:int):
    user = User.credentials_exist(username = request.form["username"], password=request.form["password"], parlor_id=id)
    if  user is not None:
        login_user(user)
        parlor = Parlor.query.get(id)
        return render_template("index.html", resp="Usuario autenticado exitósamente" ,menu=parlor.products, parlor_name=parlor.name, iden=id)
    else:
        return render_template("login.html", iden = id, message = "Credenciales erroneas")

@auth_blueprint.route("/parlor/<int:id>")
def auth(id: int):
    return render_template("login.html", iden = id)

@auth_blueprint.route("/parlor/<int:id>/user", methods=["POST"])
def create_user(id: int):
    try:
        user = User(username = request.form["username"], password=request.form["password"], parlor_id=id)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html", iden = id, message = "Usuario registrado exitósamente")
    except Exception as e:
        return "No fue posible crear el usuario" + str(e)

@auth_blueprint.route("/parlor/<int:id>/register")
def register(id: int):
    return render_template("sign_up.html", id=id)