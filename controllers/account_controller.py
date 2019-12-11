from flask import Blueprint, request, Response, redirect, url_for, render_template, jsonify, make_response
from services.account_service import is_account, create_account, strip_phone, generate_authentication, validate_authentication
from flask_jwt_extended import set_access_cookies
# TODO from services.account_services import ***

account_blueprint = Blueprint("account_api", __name__)

# Login route
@account_blueprint.route('/login', methods=["POST"])
def login():
    phone = strip_phone(request.form["phone"])
    if not is_account(phone):
        return redirect(url_for("home"))
    generate_authentication(phone)
    return render_template("authenticate.html")

# Register route
@account_blueprint.route('/register', methods=["POST"])
def register():
    phone = strip_phone(request.form["phone"])
    if not is_account(phone):
        account = create_account(request.form, phone)
    generate_authentication(phone)
    return render_template("authenticate.html")

# Authenticate route
@account_blueprint.route('/authenticate', methods=["POST"])
def authenticate():
    attempt = request.form["verification_code"]

    token, message = validate_authentication(attempt)

    resp = make_response(redirect(url_for("route_api.home")))
    set_access_cookies(resp, token)
    return resp

# Logout route
@account_blueprint.route('/logout', methods=["DELETE"])
def logout():

    # TODO build logout

    return "logout endpoint"