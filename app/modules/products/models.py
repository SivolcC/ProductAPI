"""
app/modules/products/models.py
Grouping Model classes.
"""
from app.extensions import db
import uuid


class ProductModel(db.Model):
    __tablename__ = 'Products'
    id = db.Column('Id', db.String(length=36), primary_key=True)
    name = db.Column('Name', db.String(length=17))
    description = db.Column('Description', db.String(length=35))
    price = db.Column('Price', db.Float())
    delivery_price = db.Column('DeliveryPrice', db.Float())
    # Relationship
    options = db.relationship("OptionModel", back_populates='product', cascade='all')

    def __init__(self, **kwargs):
        super(ProductModel, self).__init__(**kwargs)
        self.id = str(uuid.uuid4()).upper()

    def update(self, args):
        self.name = args.get('name', self.name)
        self.description = args.get('description', self.description)
        self.price = args.get('price', self.price)
        self.delivery_price = args.get('delivery_price', self.delivery_price)
