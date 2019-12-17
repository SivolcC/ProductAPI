"""
__init__ file of module options
"""
from app.extensions.api import api


def init_app(app, **kwargs):
    """
    Init options module.
    """
    from . import controller

    api.add_namespace(controller.ns)
