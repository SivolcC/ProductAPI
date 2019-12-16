"""
app/extensions/api/__init__.py
Initialize flask restplus api
"""
from flask_restplus import Api


api = Api(
    version='1.0.0',
    title="RefactoredXeroAPI",
    description="Refactored Xero API, from RefactorThis.",
    ordered=True,
    doc='/doc/'
)

# Temporary fix concerning https://github.com/noirbizarre/flask-restplus/issues/460
api.namespaces = []


def init_app(app, **kwargs):
    pass
