from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
# TODO bring in Amazon's authentication tool
# TODO from services.route_services import ***

route_blueprint = Blueprint("route_api", __name__)

# Home page
@route_blueprint.route('/home', methods=["GET"])
@jwt_required
def home():
    my_account = get_jwt_identity()
    print(my_account)
    # TODO render their homepage
    # TODO list any routes associated with that number

    return {
        "phone": 317
    }