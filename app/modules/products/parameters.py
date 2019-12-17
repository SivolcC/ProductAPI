"""
app/modules/products/parameters.py
Grouping Parameter classes.
"""
import marshmallow.fields as ma
from marshmallow import (validates_schema,
                         ValidationError,
                         validate)
from app.extensions.api import (Parameters,
                                SearchParameters)


class CreateProductParameters(Parameters):
    """
    Parameters to create Product
    """
    Name = ma.String(required=True, location='json', attribute='name')
    Description = ma.String(required=True, location='json', attribute='description')
    Price = ma.Float(required=True, location='json', attribute='price')
    DeliveryPrice = ma.Float(required=True, location='json', attribute='delivery_price')


class UpdateProductParameters(Parameters):
    """
    Parameters to update Product
    """
    Name = ma.String(required=False, location='json', attribute='name')
    Description = ma.String(required=False, location='json', attribute='description')
    Price = ma.Float(required=False, location='json', attribute='price')
    DeliveryPrice = ma.Float(required=False, location='json', attribute='delivery_price')


class SearchProductParameters(SearchParameters):
    """
    Parameters to search or list Products
    """
    name = ma.String(required=False, locations='querystring')
    sort_by = ma.String(
        description="Fields to be sorted. Possible choices : ['name', 'price', 'delivery_price']",
        required=False,
        location='querystring',
        validate=validate.OneOf([
            'name',
            'price',
            'delivery_price']))
