"""
app/extensions/api/webargs_parser.py
Overrides Flask webargs parser class to add error handling
Forked from https://github.com/frol/flask-restplus-server-example flask-restplus-patched folder
"""
from webargs.flaskparser import FlaskParser

from .http_exceptions import abort


class CustomWebargsParser(FlaskParser):
    """
    This custom Webargs Parser aims to overload :meth:``handle_error`` in order
    to call our custom :func:``abort`` function.

    See the following issue and the reated PR for more details:
    https://github.com/sloria/webargs/issues/122
    """

    def handle_error(self, error, *args, **kwargs):
        """
        Handles errors during parsing. Aborts the current HTTP request and
        responds with a 422 error.
        """
        status_code = getattr(error, 'status_code', self.DEFAULT_VALIDATION_STATUS)
        abort(status_code, messages=error.messages)
