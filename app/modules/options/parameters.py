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
    Name = ma.String(required=True, location='json', attribute='name')
    Description = ma.String(required=True, location='json', attribute='description')


class UpdateOptionParameters(Parameters):
    """
    Parameters to update Option
    """
    Name = ma.String(required=False, location='json', attribute='name')
    Description = ma.String(required=False, location='json', attribute='description')
