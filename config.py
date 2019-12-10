import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    AMAZON_API_KEY = os.getenv('AMAZON_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')


class Development(Config):
    DEBUG = True


class Production(Config):
    pass


class Testing(Config):
    TESTING = True


