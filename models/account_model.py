from datetime import datetime
from . import db

class Account(db.Model):
    __tablename__ = "accounts"
    phone = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String(300))
    otp_valid_until = db.Column(db.DateTime)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)

    def __init__(self, phone, fname, lname):
        self.phone = phone
        self.otp = None
        self.otp_valid_until = None
        self.fname = fname
        self.lname = lname
        now = datetime.utcnow()
        self.created_at = now
        self.last_modified = now

    # TODO determine if SAVE/DELETE on the account level are needed

    @staticmethod
    def is_account(phone):
        return Account.query.filter_by(phone=phone).first()

    