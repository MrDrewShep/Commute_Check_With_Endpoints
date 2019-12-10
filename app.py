from flask import Flask, request, jsonify
import json
from models import db
from models.account_model import Account  # only needed for db setup
from models.route_model import Route      # only needed for db setup

app = Flask(__name__)

app.config.from_object("config.Development")
db.init_app(app)

@app.route('/test', methods=["POST"])
def prelim():
    form = request.form
    return {
        "message": "hit the endpoint",
        "data": form
    }

if __name__ == "__main__":
    app.run()