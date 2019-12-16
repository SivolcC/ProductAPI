"""
app/extensions.flask_sqlalchemy/__init__.py
Initialize overriden SQLAlchemy class
"""

from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from app.extensions.constants import SQLALCHEMY_DATABASE_URI


class SQLAlchemy(BaseSQLAlchemy):
    """
    Customized Flask-SQLAlchemy adapter with enabled autocommit.
    """
    def __init__(self, *args, **kwargs):
        if 'session_options' not in kwargs:
            kwargs['session_options'] = {}
        kwargs['session_options']['autocommit'] = False
        kwargs['session_options']['autoflush'] = False
        super(SQLAlchemy, self).__init__(*args, **kwargs)

    def init_app(self, app):
        assert SQLALCHEMY_DATABASE_URI in app.config and app.config.get(SQLALCHEMY_DATABASE_URI),\
            "SQLALCHEMY_DATABASE_URI must be configured!"
        super(SQLAlchemy, self).init_app(app)
