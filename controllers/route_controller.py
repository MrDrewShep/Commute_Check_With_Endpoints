from flask import Blueprint, request, Response, redirect, url_for, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.account_service import is_account
from services.route_service import create_route
from datetime import time, timedelta
import json
import os

route_blueprint = Blueprint("route_api", __name__)

# Home page
@route_blueprint.route('/home', methods=["GET"])
@jwt_required
def home():
    my_account = is_account(get_jwt_identity())
    # TODO list any routes associated with that number

    return render_template("account_home.html", my_account=my_account)

# Build new route
@route_blueprint.route('/new', methods=["GET", "POST"])
@jwt_required
def new_route():
    my_account = is_account(get_jwt_identity())
    if request.method == "GET":
        GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
        return render_template("new_route.html", gm_api_key=GOOGLE_MAPS_API_KEY)
    elif request.method == "POST":
        form_data = request.form
        google_response = json.loads(form_data["google_response"])
        return google_response
        return form_data["google_response"]["request"]["origin"]["query"]
        return create_route(my_account, form_data)
        