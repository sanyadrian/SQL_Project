import pytest
from webtest import TestApp

from main import create_app
from src.db.models import db as _db
from src.config import TestConfig
from flask_sqlalchemy import SQLAlchemy



@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    with _app.app_context():
        _db.init_app(_app)
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()



@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        # _db = SQLAlchemy(app)
        # _db.init_app(app)
        _db.create_all()
    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def client(app):
    """A user for the tests."""
    return app.test_client()