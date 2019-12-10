from flask import Blueprint, request, Response, redirect, url_for
# TODO Need amazon's text message token service here
# TODO from services.account_services import ***

auth_blueprint = Blueprint("auth_api", __name__)

# Register route
@auth_blueprint.route('/register', methods=["POST"])
def register():
    data = request.json
    

# Login route
@auth_blueprint.route('/login', methods=["POST"])
def login():
    data = request.json

    # TODO Run text message authentication code here
    # TODO Redirect user to field to input code
        # TODO Validate and redirect to account/home or /login

    return None

# Logout route
@auth_blueprint.route('/logout', methods=["DELETE"])
def logout():

    # TODO build logout

    return None