from flask import Blueprint, request, Response, redirect, url_for, render_template
from services.account_service import is_account, create_account, strip_phone, generate_authentication, validate_authentication
# TODO from services.account_services import ***

account_blueprint = Blueprint("account_api", __name__)

# Login route
@account_blueprint.route('/login', methods=["POST"])
def login():
    data = request.json

    # TODO Run text message authentication code here
    # TODO Redirect user to field to input code
        # TODO Validate and redirect to account/home or /login

    return None

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
    return {
        "token": token,
        "message": message
    }

# Logout route
@account_blueprint.route('/logout', methods=["DELETE"])
def logout():

    # TODO build logout

    return None