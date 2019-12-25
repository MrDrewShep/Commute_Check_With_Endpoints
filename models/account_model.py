from datetime import datetime
from . import db

class Account(db.Model):
    __tablename__ = "accounts"
    phone = db.Column(db.String(15), primary_key=True)
    otp = db.Column(db.String(300))
    otp_expiration = db.Column(db.DateTime)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)

    def __init__(self, phone, fname, lname):
        self.phone = phone
        self.otp = None
        self.otp_expiration = None
        self.fname = fname
        self.lname = lname
        now = datetime.utcnow()
        self.created_at = now
        self.last_modified = now

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, to_change):
        for key, value in to_change.items():
            setattr(self, key, value)
        self.last_modified = datetime.utcnow()
        db.session.commit()
        return self

    @staticmethod
    def get_account(phone):
        return Account.query.filter_by(phone=phone).first()

    