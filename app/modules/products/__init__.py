"""
app/modules/products/__init__.py
"""
from app.extensions.api import api


def init_app(app, **kwargs):
    """
    Init products module.
    """
    from . import controller

    api.add_namespace(controller.ns)
