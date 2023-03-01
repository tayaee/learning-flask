import pytest
from flask import Flask
from flask import g
from flask import session
from flask.testing import FlaskClient

from flaskr.db import get_db
from tests.conftest import AuthActions


# Test /auth/register
def test_register(client: FlaskClient, app: Flask):
    res = client.get('/auth/register')
    assert res.status_code == 200

    res = client.post('/auth/register', data={'username': 'a', 'password': 'a'})
    location = res.headers['Location']
    assert location == '/auth/login'

    with app.app_context():  # TODO Learn more about this
        db = get_db()
        sql = 'select * from user where username = ?'
        args = ('a',)
        row = db.execute(sql, args).fetchone()
        if row is not None:
            user = {k: row[k] for k in row.keys()}
        assert row is not None


# Test /auth/register with negative cases
@pytest.mark.parametrize(('username', 'password', 'message'),
                         (
                                 ('', '', b'Username is required.'),
                                 ('a', '', b'Password is required.'),
                                 ('test', 'test', b'already registered'),
                         )
                         )
def test_register_validate_input(client: FlaskClient, username: str, password: str, message: str):
    data = {'username': username, 'password': password}
    res = client.post('/auth/register', data=data)
    assert message in res.data


# Test /auth/login
def test_login(client: FlaskClient, auth: AuthActions):
    res = client.get('/auth/login')
    assert res.status_code == 200

    res = auth.login()  # Log in as test/test
    location = res.headers['Location']
    assert location == '/'

    with client:  # TODO Learn more about this
        client.get('/')
        session_user_id = session['user_id']
        assert 1 == session_user_id
        g_user_username = g.user['username']
        assert 'test' == g_user_username


# Test /auth/login with negative cases
@pytest.mark.parametrize(('username', 'password', 'expected_message'),
                         (
                                 ('', '', b'Username is required.'),
                                 ('any', '', b'Password is required.'),
                                 ('wrong', 'test', b'Incorrect username.'),
                                 ('test', 'wrong', b'Incorrect password.'),
                         )
                         )
def test_login_validate_input(auth: AuthActions, username: str, password: str, expected_message: str):
    res = auth.login(username, password)
    print(res.data)
    assert expected_message in res.data


def test_logout(client: FlaskClient, auth: AuthActions):
    # session_user_id = session.get('user_id')
    # assert 'user_id' not in session

    auth.login()
    # assert 'user_id' in session

    with client:
        auth.logout()
        assert 'user_id' not in session
