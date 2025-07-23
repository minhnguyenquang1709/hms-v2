# responsible for setting up the test database and creating the FastAPI application for testingimport asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.testing.entities import ComparableEntity

from src.main import init_app
from src.api.v1.models import *
from src.config.db import session_manager, get_db


# fixtures provide a fixed baseline so that tests execute reliably and produce consistent, repeatable results
@pytest.fixture(autouse=True)  # activate this fixture for all tests that can see it
def app():
    with ExitStack():
        yield init_app(
            init_db=False
        )  # manually initialize database connection & create the test database


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c

test_db = factories.postgresql_proc(port=None, dbname="test_db")