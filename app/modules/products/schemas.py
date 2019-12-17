"""
app/modules/products/schemas.py
Grouping Schema classes.
"""
import marshmallow.fields as ma
from app.extensions.api import ModelSchema
from .models import ProductModel


class ProductSchema(ModelSchema):
    id = ma.Str(dump_to='Id')
    name = ma.Str(dump_to='Name')
    description = ma.Str(dump_to='Description')
    price = ma.Float(dump_to='Price')
    delivery_price = ma.Float(dump_to='DeliveryPrice')


class PaginatedProductSchema(ModelSchema):
    """
    Paginated event_user hybrid schema
    """
    page = ma.Integer()
    pages = ma.Integer()
    per_page = ma.Integer()
    total = ma.Integer()
    items = ma.Nested(ProductSchema, many=True, dump_to='Items')
