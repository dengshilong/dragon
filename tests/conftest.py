import os

import pytest

from dragon import Dragon


@pytest.fixture
def app():
    app = Dragon(__name__)
    return app


@pytest.fixture
def client(app):
    return app.test_client()