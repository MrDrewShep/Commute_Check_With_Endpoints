from flask import Flask, request, jsonify, render_template, redirect
import json
from models import db
from services import jwt
from controllers import account_blueprint, route_blueprint
from models.account_model import Account  # only needed for db setup
from models.route_model import Route      # only needed for db setup

app = Flask(__name__)

app.config.from_object("config.Development")
db.init_app(app)
jwt.init_app(app)

app.register_blueprint(account_blueprint, url_prefix="/account")
app.register_blueprint(route_blueprint, url_prefix="/route")

@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()