"""
app/modules/products/controller.py
Grouping Resource classes.
"""
from app.extensions import db
from app.extensions.api import (Namespace,
                                Resource)
from .schemas import (ProductSchema,
                      PaginatedProductSchema)
from .models import ProductModel
from .parameters import (SearchProductParameters,
                         CreateProductParameters,
                         UpdateProductParameters)

ns = Namespace('products',
               ordered=True,
               description="Namespace for the 'Product' resource.")


@ns.route('')
class ProductResource(Resource):
    @ns.parameters(SearchProductParameters())
    @ns.response(PaginatedProductSchema())
    def get(self, args):
        """
        Get paginated list of Products.
        Search by name
        Sort by name, price or delivery price
        """
        product_search_query = ProductModel.query
        if args.get('name'):
            product_search_query = product_search_query\
                .filter(ProductModel.name.ilike("%" + args['name'] + "%"))
        if args.get('sort_by'):
            product_search_query = product_search_query.order_by(
                getattr(getattr(ProductModel, args.get('sort_by')), args.get('sort_direction'))())
        return product_search_query.paginate(args['page'], args['per_page'], False)

    @ns.parameters(CreateProductParameters())
    @ns.response(ProductSchema())
    def post(self, args):
        """
        Creates a Product
        """
        product = ProductModel(**args)
        db.session.add(product)
        return product


@ns.route('/<string:product_id>')
@ns.resolve_object_by_model(ProductModel, 'product')
class ProductByIDResource(Resource):
    @ns.response(ProductSchema())
    def get(self, product):
        """
        Get product details by Id.
        """
        return product

    @ns.parameters(UpdateProductParameters())
    @ns.response(ProductSchema())
    def put(self, args, product):
        """
        Put product details by Id.
        """
        product.update(args)
        return product

    def delete(self, product):
        """
        Delete a product by Id.
        """
        db.session.delete(product)
        return None, 204
