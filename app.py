from flask import Flask, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user

from controllers.parlor_controller import parlor_blueprint
from controllers.auth_controller import auth_blueprint
from controllers.ingredient_controller import ingredient_blueprint
from controllers.product_controller import product_blueprint
import os
from urllib.parse import quote_plus
from db.db import db, init_db
from db.init_data import fill_db
from models.parlor import Parlor
from models.users import User

secret_key = os.urandom(24)

app = Flask(__name__, template_folder="views")
app.register_blueprint(parlor_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(ingredient_blueprint)
app.register_blueprint(product_blueprint)
app.config["SECRET_KEY"] = secret_key

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    users_db = User.query.all()
    for user in users_db:
        if user.id == int(user_id):
            return user
    return None

@app.route("/")
def index():
    parlors = Parlor.query.all()
    return render_template("welcome.html", parlors=parlors)

# app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{os.getenv("DB_USER_NAME")}:{quote_plus(os.getenv("DB_PASSWORD"))}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join('/tmp', 'project.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)

# init_db(app) # Si no se tiene una base de datos con los objetos, se debe descomentar esto y correr la aplicación
# fill_db(app, db)

if __name__ == '__main__':
    app.run(debug=True)