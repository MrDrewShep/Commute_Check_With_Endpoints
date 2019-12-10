from models.account_model import Account
from flask_jwt_extended import create_access_token
from . import bcrypt
from random import randint
from datetime import datetime

def create_otp(phone):
    otp = randint(1000,9999)
    otp_hash = bcrypt.generate_password_hash(otp).decode("utf-8")
    otp_expiration = datetime.now() + 60*5
    return otp, otp_hash, otp_expiration

def create_account(phone, fname, lname):
    if not Account.is_account(phone):
        print('not yet an account')