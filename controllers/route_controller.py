from flask import Blueprint, request, Response
# TODO bring in Amazon's authentication tool
# TODO from services.route_services import ***

route_blueprint = Blueprint("route_api", __name__)

# Home page
@route_blueprint.route('/home', methods=["GET"])
def home():

    # TODO render their homepage
    # TODO list any routes associated with that number

    return None