"""
schemas.py file of module options.
Grouping Schema classes.
"""
import marshmallow.fields as ma
from app.extensions.api import ModelSchema
from app.modules.products.schemas import ProductSchema
from .models import OptionModel


class OptionSchema(ModelSchema):
    id = ma.Str(dump_to='Id')
    name = ma.Str(dump_to='Name')
    description = ma.Str(dump_to='Description')
    # product = ma.Nested(ProductSchema, dump_to='Product')


class PaginatedOptionSchema(ModelSchema):
    """
    Paginated event_user hybrid schema
    """
    page = ma.Integer()
    pages = ma.Integer()
    per_page = ma.Integer()
    total = ma.Integer()
    items = ma.Nested(OptionSchema, many=True, dump_to='Items')
