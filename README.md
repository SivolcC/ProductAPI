Refactored RESTful ProductAPI
=============================


## Considerations regarding the initial project

This project is part of a technical assessment, the goal is to refactor an API written in .NET.
You can find the initial README [here](README.deprecated.md)

The initial API, named RefactorThis was "poorly written" and lacked of what is a real production-ready project:

#### No unit tests:
It is fundamental to have a minimum of automated testing for production code.
It saves a lot of time and potential downtime if unit tests are ran before each merge or deployment.
Ideally, in with Agile methods, and particularly Test Driven Development, unit tests should be written before the code itself.

#### Endpoints returning lists not paginated:
While it may be okay for some endpoints returning list of object to be not paginated (for example a fixed list of objects),
RefactorThis API was returning an un-paginated list of Products. It may be fine for short term, but this is not scalable at all:
if the database grows and the number of products increase to few hundreds, the latency and the size of payloads will explode.
There is alternatives to pagination, such as streams, websockets, or queues. But from a RESTful perspective, and for the sake of simplicity, pagination is a better option.
Of course with pagination comes sorting. The ProductAPI handles sorting on paginated endpoints.

#### RESTful concepts implemented inconsistently:
It is okay to have endpoints designed like this:
`GET /products/{id}/options/{optionId}` - finds the specified product option for the specified product.
But `GET /options/{optionId}` makes more sense, since `optionId` is a primary key, and we do not need `productId` to get the `Option` object.
ProductAPI now implements the `options/` namespace that fixes those inconsistencies.
From a perspective of the consumers of the API, it would be necessary to update the way they are using those endpoints.
While this is a breaking change, it would eventually be possible to re-implement endpoints like `GET /products/{id}/options/{optionId}`, but ignoring the `productId`

#### Lack of documentation, and code comments:
Production quality code must have comments and documentation.
Thanks to `flask-restplus` framework, ProductAPI now has an interactive API documentation based on OpenAPI, formerly known as Swagger.
While this should not be made public in production (unless you want your API to be public), it is a standardized way to share API specs to other developers.

RefactorThis API was lacking comments in the code. For developers who did not have previous exposure, it can be very hard to catch-up.

## Future possible improvements

#### Better Nginx configuration:
ProductAPI uses Nginx as reverse proxy. The current Nginx configuration is very simplistic and depending on the infrastructure behind, should implement security best practices like security headers.

#### Choices regarding SSL termination:
For the sake of simplicity, ProductAPI doesn't implement SSL.
SSL termination can be handled by multiple layers of the app : flask, gunicorn or nginx. But many Cloud platforms can handle SSL termination at other levels (load balancer, container orchestration service...).
Decrypting https requests can add significant load to the CPU, and it may be preferable to deploy the containers behind a layer of the infrastructure that handles SSL termination, such as AWS Application Load Balancer, API Gateway/Cloudfront or Google Cloud SSL Proxy Load Balancing

#### Authentication:
Authentication is also crucial.
To avoid complexity in the context of this assessment, ProductAPI does not implements any sort of authentication system. And it would be mandatory to implement one for a production release.
Authentication can eventually be handled in other layers in the system, such as on the Cloud platform. AWS, GoogleCloud and Azure propose different services for that such as AWS Cognito.

#### Logging and monitoring
Various frameworks handle logging and monitoring quite well, and it is often a good choice for production systems to use a third-party service like Sentry, NewRelic, or even the ones of the Cloud provider like AWS CloudWatch or Azure Monitor

#### Database engine:
SQLite is not a production-ready database engine, it is not easily scalable and does not support concurrency.
While it is a great choice in the context of this project (educational and training), a real production-ready project would use a real Client/Server RDBMS like PostgreSQL.

#### Secret and dynamically loaded environment variables.
Having a file containing the environment variables necessary for the app is not good practice.
The file could contain sensitive data (such as database connection string, or third-party API keys) and the variables should not be accessible outside of the context of the app.
In the context of a containerized application, Cloud providers propose various solutions on how to handle secret variables such as AWS Secret Manager integrated in AWS ECS task definitions.


# Quickstart

Set up local environment
------------------------
If you are in a Windows environment, `gunicorn` being incompatible, we cannot guaranty that ProductAPI will work outside of its docker container (for that, jump to "Run with Docker" section).
You will have to look into [`Waitress`](https://docs.pylonsproject.org/projects/waitress/en/latest/) to host the flask app on Windows.

If you are in a UNIX environment, to get started quickly with the project, set up a virtual environment, recommended way is virtualenv.

`virtualenv -p <path to python3.7+ binary> env`

`source env/bin/activate`

`pip install -r requirements.txt`

Start up server
---------------

`gunicorn -b 0.0.0.0:5000 wsgi:app`

Open online interactive API documentation:
[http://127.0.0.1:5000/api/doc](http://127.0.0.1:5000/api/doc)

Autogenerated OpenAPI config is always available at
[http://127.0.0.1:5000/api/swagger.json](http://127.0.0.1:5000/api/swagger.json)




# Project details

Project Structure
-----------------

This project is a fork of https://github.com/frol/flask-restplus-server-example.
It uses the same file hierarchy, and implements the patched flask-restplus dependency, but differs in many other points, since ProductAPI is a much more simplistic project.

### Root folder

Folders:

* `app` - RESTful API implementation is here.
* `deployment_config` - Folder used to store various deployment configuration files (reverse proxy, gunicorn)

Files:

* `README.md`
* `run.py` - Entrypoint of the app.
* `config.py` - Config file of the app.
* `requirements.txt` - The list of Python (PyPi) requirements.
* `Dockerfile` - Dockerfile for the API.
* `docker-compose.yml` - Docker compose file to run API container and reverse proxy (Nginx) container.
* `entrypoint.sh` - File used by docker to start the API.
* `var.env` - File grouping environment variables to be used in the API container

### Application Structure

```
app/
├── __init__.py
├── extensions
│   └── __init__.py
└── modules
    ├── __init__.py
    ├── api
    │   └── __init__.py
    └── product
        ├── __init__.py
        ├── models.py
        ├── parameters.py
        ├── test_products_module.py
        ├── resources.py
        └── schemas.py
```

* `app/__init__.py` - The entrypoint to the API
  application (Flask application is created here).
* `app/extensions` - All extensions (e.g. SQLAlchemy, ...) are initialized
  here and can be used in the application by importing as, for example,
  `from app.extensions import db`.
* `app/modules` - All endpoints are expected to be implemented here in logically
  separated modules.

### Module Structure

Once you added a module name into `config.ENABLED_MODULES` (module `api` must be last of the list),
it is required to have `your_module.init_app(app, **kwargs)` function.
Thus, here is the required minimum:

```
your_module/
└── __init__.py
```

, where `__init__.py` will look like this:

```python
def init_app(app, **kwargs):
    pass
```

In this example, however, `init_app` imports `resources` and registers `api`
(an instance of (patched) `flask_restplus.Namespace`). Learn more about the
"big picture" in the next section.

Runtime
-------

The server is started by this command:

`$ gunicorn -b 0.0.0.0:5000 run:app`

The command calls `run.py` file that creates an application by running
[`app/__init__.py:create_app()`](app/__init__.py) function, which in its turn:

1. loads an application config;
2. initializes extensions:
   [`app/extensions/__init__.py:init_app()`](app/extensions/__init__.py);
3. initializes modules:
   [`app/modules/__init__.py:init_app()`](app/modules/__init__.py).

Modules initialization calls `init_app()` in every enabled module
(listed in `config.ENABLED_MODULES`).

Let's take `products` module as an example to look further.
[`app/modules/products/__init__.py:init_app()`](app/modules/products/__init__.py)
imports and registers `api` instance of (patched) `flask_restplus.Namespace`
from `.resources`. Flask-RESTPlus `Namespace` is designed to provide similar
functionality as Flask `Blueprint`.

Lastly, every `Resource` should have methods which are lowercased HTTP method
names (i.e. `.get()`, `.post()`, etc). This is where users' requests end up.


Testing
-------

To test the application, we use `pytest`.
The files `test_[module_name]_module.py` (should!) contains tests for every endpoint of the module's `resource.py`.
`conftest.py` contains fixtures for existing tests.

To run the tests:

`$ pytest -v -W ignore::DeprecationWarning -l --tb=line -x`

This command will run the tests while ignoring deprecation warnings (usually coming from dependencies) and printing errors on a single line.
To get a more detailed output, remove the `--tb=line` argument.

More infos on how pytest works [**here**](https://docs.pytest.org/en/latest/)


Run with Docker
---------------

This project uses docker-compose to orchestrate the api container along a reverse proxy container.

You can execute the build command from the root of the repository:
`$ docker-compose build`

Before running the containers, it is recommended to double check the env variables contained in var.env file.

You can now run the container:
``$ docker-compose up``

You can now browse http://localhost/api/doc :)


Dependencies
------------

### Project Dependencies

* [**Python**](https://www.python.org/) 3.7+
* [**flask-restplus**](https://github.com/noirbizarre/flask-restplus) (+
  [*flask*](http://flask.pocoo.org/))
* [**sqlalchemy**](http://www.sqlalchemy.org/) (+
  [*flask-sqlalchemy*](http://flask-sqlalchemy.pocoo.org/)) - Database ORM.
* [**marshmallow**](http://marshmallow.rtfd.org/) (+
  [*marshmallow-sqlalchemy*](http://marshmallow-sqlalchemy.rtfd.org/),
  [*flask-marshmallow*](http://flask-marshmallow.rtfd.org/)) - for
  schema definitions. (*supported by the patched Flask-RESTplus*)
* [**webargs**](http://webargs.rtfd.org/) - for parameters (input arguments).
  (*supported by the patched Flask-RESTplus*)
* [**apispec**](http://apispec.rtfd.org/) - for *marshmallow* and *webargs*
  introspection. (*integrated into the patched Flask-RESTplus*)
* [**Gunicorn**](http://gunicorn.org/) - Recommended HTTP server.

### Patched Dependencies

* **flask-restplus** is patched to handle marshmallow schemas and webargs
  input parameters.
  ([GH #9](https://github.com/noirbizarre/flask-restplus/issues/9)).
  The overriden classes can be found in `/app/extension/api/`:

* `Parameters` - base class, which is a thin
  wrapper on top of Marshmallow Schema.
* `Namespace.parameters` - a helper decorator,
  which automatically handles and documents the passed `Parameters`.

You can find the examples of the usage throughout the code base (in
`/app/modules/*`).
