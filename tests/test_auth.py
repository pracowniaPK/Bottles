import pytest
from flask import g, session
from bottles.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'nick':'a', 'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM user WHERE username = "a"'
        ).fetchone() is not None

@pytest.mark.parametrize(
    'nick,username,password,message',
    [('', '', '', b'Nick required'),
    ('a', '', '', b'Username required'),
    ('a', 'a', '', b'Passwd required'),
    ('test_nick', 'test', 'test',  b'Nick test_nick is already taken.'),
    ('test', 'test', 'test', b'User test is already registered.'),
    ])
def test_register_validate_input(client, nick, username, password, message):
    response = client.post(
        '/auth/register',
        data={'nick': nick, 'username': username, 'password': password}
    )
    print(response.data)
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        print(g.user['nick'])
        print(g.user['username'])
        assert session['user_id'] == 1
        assert g.user['nick'] == 'test_nick'
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(
    ('username,password,message'),
    [('test', 'a', b'Incorrect password.'),
    ('a', 'test', b'Incorrect username.')]
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session