import os


class BaseConfig(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    ERROR_404_HELP = False

    ENABLED_MODULES = (
        'products',
        'options',
        'api',
    )

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

    SWAGGER_UI_JSONEDITOR = True

    DEBUG = False
    TESTING = False


class RemoteConfig(BaseConfig):
    FLASK_CONFIG =                   os.getenv('FLASK_CONFIG')

    # ORM
    SQLALCHEMY_DATABASE_URI =        os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')


class DevelopmentConfig(BaseConfig):
    FLAKS_CONFIG =                   'development'

    # ORM
    SQLALCHEMY_DATABASE_URI =        'sqlite:///../database/products.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
