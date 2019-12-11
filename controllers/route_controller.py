from flask import Blueprint, request, Response, redirect, url_for, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.account_service import is_account
from services.route_service import create_route
from datetime import time, timedelta
# TODO from services.route_services import ***

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
        return render_template("new_route.html")
    elif request.method == "POST":
        data = request.form
        # tm = data["local_run_time"]
        # print(tm, type(tm))
        # tmm = time(int(tm[:2]) - int(data["local_timezone_offset"]), int(tm[3:]))
        # print(tmm, type(tmm))
        # return "end"
        return data
        return create_route(my_account, data)
        