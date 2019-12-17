"""
controller.py file of module options.
Grouping Resource classes.
"""
from app.extensions.api import (Namespace,
                                Resource,
                                Parameters)
from app.extensions import db

from .schemas import (OptionSchema,
                      PaginatedOptionSchema)
from .models import OptionModel
from .parameters import (CreateOptionParameters,
                         UpdateOptionParameters)

ns = Namespace('options',
               ordered=True,
               description="Namespace for the 'Option' resource.")


@ns.route('/<string:option_id>')
@ns.resolve_object_by_model(OptionModel, 'option')
class OptionByIDResource(Resource):
    @ns.response(OptionSchema())
    def get(self, option):
        """
        Get option details by Id.
        """
        return option

    @ns.parameters(UpdateOptionParameters())
    @ns.response(OptionSchema())
    def put(self, args, option):
        """
        Put option details by Id.
        """
        option.update(args)
        return option

    def delete(self, option):
        """
        Delete a option by Id.
        """
        db.session.delete(option)
        return None, 204
