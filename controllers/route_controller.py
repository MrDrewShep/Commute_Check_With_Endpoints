from flask import Blueprint, request, Response, redirect, url_for, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.account_service import is_account
from services.route_service import create_route, get_all_routes, toggle_route_active_status
from datetime import time, timedelta
import json
import os
from services.route_service import parse_waypoints  # TODO delete once ready

route_blueprint = Blueprint("route_api", __name__)

# Home page
@route_blueprint.route('/home', methods=["GET"])
@jwt_required
def home():
    my_account = is_account(get_jwt_identity())
    my_routes = get_all_routes(my_account.phone)
    return render_template("account_home.html", my_account=my_account, my_routes=my_routes)

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
        create_route(my_account, form_data)
        return redirect(url_for("route_api.home"))

# Toggle whether a route is active/inactive
@route_blueprint.route('/toggle_active_status/<int:route_id>')
@jwt_required
def toggle_active_status(route_id):
    my_account = is_account(get_jwt_identity())
    toggle_route_active_status(my_account, route_id)
    return redirect(url_for("route_api.home"))

