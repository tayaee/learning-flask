import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db

data_sql_file = os.path.join(os.path.dirname(__file__), 'data.sql')
with open(data_sql_file, 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})
    with app.app_context():
        init_db()
        db = get_db()
        db.executescript(_data_sql)
    yield app  # TODO Learn more about this
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()  # TODO Learn more


@pytest.fixture
def runner(app):
    return app.test_cli_runner()  # TODO Learn more


# Test auth
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        res = self._client.post('/auth/login', data={'username': username, 'password': password})
        return res

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
