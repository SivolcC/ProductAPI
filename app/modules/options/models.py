"""
models.py file of module options.
Grouping Model classes.
"""
from app.extensions import db
import uuid


class OptionModel(db.Model):
    __tablename__ = 'ProductOptions'
    id = db.Column('Id', db.String(length=36), primary_key=True)
    name = db.Column('Name', db.String(length=9))
    description = db.Column('Description', db.String(length=23))
    # Relationships
    product_id = db.Column('ProductId', db.String(length=36), db.ForeignKey('Products.Id'))
    product = db.relationship('ProductModel', back_populates='options')

    def __init__(self, **kwargs):
        super(OptionModel, self).__init__(**kwargs)
        self.id = str(uuid.uuid4()).upper()

    def update(self, args):
        self.name = args.get('name', self.name)
        self.description = args.get('description', self.description)
