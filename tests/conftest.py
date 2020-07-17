import os
import tempfile

import pytest
from unittest.mock import patch

from bottles import create_app
from bottles.db import init_db
from data import create_test_data


class AuthAction:
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthAction(client)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    db_path_sqlized = 'sqlite:///' + db_path
    # env_vars = {'SECRET_KEY': 'dev', 'DATABASE_URI': db_path_sqlized}
    # with patch.dict('os.environ', env_vars):
    os.environ['DATABASE_URI'] = db_path_sqlized
    app = create_app({
        'TESTING': True,
        'DATABASE_URI': db_path_sqlized,
    })

    with app.app_context():
        init_db()
        create_test_data()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
