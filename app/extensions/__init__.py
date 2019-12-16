"""
app/extensions/__init__.py
Initialize extensions
"""

from . import api

def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
        api,
    ):
        extension.init_app(app)
