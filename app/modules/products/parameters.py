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
    name = ma.String(equired=True, location='json', dump_to='Name')
    description = ma.String(required=True, location='json', dump_to='Description')
    price = ma.Float("Price", required=True, location='json', dump_to='Price')
    delivery_price = ma.Float("DeliveryPrice", required=True, location='json', dump_to='DeliveryPrice')


class UpdateProductParameters(Parameters):
    """
    Parameters to update Product
    """
    name = ma.String(required=False, location='json', dump_to='Name')
    description = ma.String(required=False, location='json', dump_to='Description')
    price = ma.Float(required=False, location='json', dump_to='Price')
    delivery_price = ma.Float(required=False, location='json', dump_to='DeliveryPrice')


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
