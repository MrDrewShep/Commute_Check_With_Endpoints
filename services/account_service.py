from models.account_model import Account
from flask_jwt_extended import create_access_token
from . import bcrypt
from random import randint
from datetime import datetime, timedelta
from send_sms import send_sms

def create_otp():
    otp = str(randint(1000,9999))
    otp_hash = bcrypt.generate_password_hash(otp).decode("utf-8")
    otp_expiration = datetime.utcnow() + timedelta(minutes=5)
    return otp, otp_hash, otp_expiration

def is_account(phone):
    return Account.get_account(phone)

def strip_phone(phone):
    new_phone = ""
    for i in phone:
        try:
            int(i)
            new_phone += i
        except:
            pass
    return new_phone

def create_account(data, phone):
    new_account = Account(phone, data["fname"], data["lname"])
    try:
        message = new_account.save()
    except Exception as e:
        message = str(e)
    return message

def generate_authentication(phone):
    account = is_account(phone)

    otp, otp_hash, otp_expiration = create_otp()
    otp_data = {
        "otp": otp_hash,
        "otp_expiration": otp_expiration
    }
    account.update(otp_data)

    e164_phone = "+1" + phone
    text_message = f'Your commute check verification code is {otp}.'
    send_sms(e164_phone, text_message)

    return "otp updated"

def validate_authentication(attempt):
    message = "Login failed."
    token = "No token provided."

    my_account = is_account("3175142678")       # TODO make this modular

    if my_account:
        if datetime.utcnow() < my_account.otp_expiration:
            if bcrypt.check_password_hash(my_account.otp, attempt):
                token = create_access_token(identity=my_account.phone)
                message = "Successfully authenticated."
            else:
                message = "Incorrect code."
        else:
            message = "Time has expired."
    return token, message
    



