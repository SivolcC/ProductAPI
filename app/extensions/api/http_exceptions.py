"""
app/extensions/api/http_exceptions.py
Overrides Flask-Restplus abort() method
Forked from https://github.com/frol/flask-restplus-server-example flask-restplus-patched folder
"""
from flask_restplus.errors import abort as restplus_abort
from flask_restplus._http import HTTPStatus


API_DEFAULT_HTTP_CODE_MESSAGES = {
    HTTPStatus.UNAUTHORIZED.value: (
        "The server could not verify that you are authorized to access the "
        "URL requested. You either supplied the wrong credentials (e.g. a bad "
        "password), or your browser doesn't understand how to supply the "
        "credentials required."
    ),
    HTTPStatus.FORBIDDEN.value: (
        "You don't have the permission to access the requested resource."
    ),
    HTTPStatus.UNPROCESSABLE_ENTITY.value: (
        "The request was well-formed but was unable to be followed due to semantic errors."
    ),
}


def abort(code, message=None, **kwargs):
    """
    Custom abort function used to provide extra information in the error
    response, namely, ``status`` and ``message`` info.
    """
    if message is None:
        if code in API_DEFAULT_HTTP_CODE_MESSAGES:
            message = API_DEFAULT_HTTP_CODE_MESSAGES[code]
        else:
            message = HTTPStatus(code).description
    restplus_abort(code=code, status=code, message=message, **kwargs)
