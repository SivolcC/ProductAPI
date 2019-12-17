"""
parameters.py file of module options.
Grouping Parameter classes
"""
import marshmallow.fields as ma
from marshmallow import (validates_schema,
                         ValidationError,
                         validate)
from app.extensions.api import Parameters


class CreateOptionParameters(Parameters):
    """
    Parameters to create Option
    """
    name = ma.String(required=True, location='json', dump_to='Name')
    description = ma.String(required=True, location='json', dump_to='Description')


class UpdateOptionParameters(Parameters):
    """
    Parameters to update Option
    """
    name = ma.String(required=False, location='json', dump_to='Name')
    description = ma.String(required=False, location='json', dump_to='Description')
