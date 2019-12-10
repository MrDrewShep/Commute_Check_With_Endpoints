import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    DEBUG = True


class Production(Config):
    pass


class Testing(Config):
    TESTING = True


