import pytest
from bs4 import BeautifulSoup as bs
from flask import Flask
from flask.testing import FlaskClient

from flaskr.db import get_db
from tests.conftest import AuthActions


def test_index(client: FlaskClient, auth: AuthActions):
    # arrange
    res = client.get('/')
    assert res.status_code == 200
    assert b'Register' in res.data
    assert b'Log In' in res.data

    # act
    res = auth.login()
    assert res.status_code == 302

    # assert
    res = client.get('/')
    assert res.status_code == 200
    assert b'Log Out' in res.data


@pytest.mark.parametrize('path', (
        '/create',
        '/1/update',
        '/1/delete',
))
def test_login_required(client: FlaskClient, path: str):
    # act
    res = client.post(path)

    # assert
    location = res.headers['Location']
    assert location == '/auth/login'


def test_author_required(app: Flask, client: FlaskClient, auth: AuthActions):
    # arrange
    with app.app_context():
        db = get_db()
        db.execute('update post set author_id = 2 where id = 1')
        db.commit()
    auth.login(username='test', password='test')

    # act
    res = client.post('/1/update')

    # assert
    assert res.status_code == 403

    # act
    res = client.post('/1/delete')

    # assert
    assert res.status_code == 403


def test_exists_required(client: FlaskClient, auth: AuthActions):
    auth.login()

    # I can delete mine.
    res = client.post('/1/delete')
    print(str(bs(res.data.decode())))
    assert res.status_code == 302

    # I cannot delete a post that does not exist.
    res = client.post('/2/delete')
    print(str(bs(res.data.decode())))
    assert res.status_code == 404


def test_create(client: FlaskClient, auth: AuthActions, app: Flask):
    # The # of posts is 1
    with app.app_context():
        db = get_db()
        sql = 'select count(id) from post'
        row = db.execute(sql).fetchone()
        assert row[0] == 1

    res = auth.login()
    assert res.status_code == 302

    res = client.get('/create')
    assert res.status_code == 200

    data = {'title': 'created', 'body': ''}
    res = client.post('/create', data=data)
    assert res.status_code == 302  # redirect to /index if post is successful

    # The # of posts is now 2
    with app.app_context():
        db = get_db()
        sql = 'select count(id) from post'
        row = db.execute(sql).fetchone()
        assert row[0] == 2


def test_update(client: FlaskClient, auth: AuthActions, app: Flask):
    with app.app_context():
        db = get_db()
        sql = 'select * from post where id = 1'
        row = db.execute(sql).fetchone()
        title = row['title']
        assert title == 'test title'

    res = auth.login()
    assert res.status_code == 302  # go to /

    res = client.get('/1/update')
    assert res.status_code == 200

    data = {'title': 'updated', 'body': ''}
    res = client.post('/1/update', data=data)
    assert res.status_code == 302  # go to /

    with app.app_context():
        db = get_db()
        sql = 'select * from post where id = 1'
        row = db.execute(sql).fetchone()
        title = row['title']
        assert title == 'updated'


@pytest.mark.parametrize('path', ('/create', '/1/update'))
def test_create_update_validate(client, auth, path):
    res = auth.login()
    assert res.status_code == 302

    res = client.post(path, data={'title': '', 'body': ''})
    assert res.status_code == 200  # is 201 better?
    assert b'Title is required.' in res.data


def test_delete(client, auth, app):
    with app.app_context():
        db = get_db()
        sql = 'select * from post where id = 1'
        row = db.execute(sql).fetchone()
        assert row is not None

    res = auth.login()
    assert res.status_code == 302

    res = client.post('/1/delete')
    assert res.status_code == 302
    location = res.headers['Location']
    assert location == '/'

    with app.app_context():
        db = get_db()
        sql = 'select * from post where id = 1'
        row = db.execute(sql).fetchone()
        assert row is None


def test_delete_failure(client, auth):
    res = auth.login()
    assert res.status_code == 302

    res = client.post('/2/delete')
    assert res.status_code == 404
