import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AMAZON_API_KEY = os.getenv('AMAZON_API_KEY')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_CSRF_PROTECT = False


class Development(Config):
    DEBUG = True


class Production(Config):
    pass


class Testing(Config):
    TESTING = True


