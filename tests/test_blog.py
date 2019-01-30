import pytest


def test_index(client, auth):
    response = client.get('/', follow_redirects=True)
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'my title' in response.data
    assert b'my post content' in response.data
    assert b'by test' in response.data

def test_create_post(client, auth):
    response = client.get('/new')
    assert response.headers['Location'] == 'http://localhost/auth/register'

    auth.login(username='test2', password='test2')
    assert client.get('/new').status_code == 200
    response = client.post('/', 
        data={'title':'testing title','body':'testing body'})
    auth.logout()

    auth.login()
    response = client.get('/')
    print(response.data)
    assert b'testing title' in response.data
    assert b'testing body' in response.data

def test_post_validation(client, auth):
    auth.login(username='test2', password='test2')
    response = client.post('/', data={'title':'','body':'empty title'})
    assert b'Title required' in response.data
    response = client.post('/', data={'title':'empty body','body':''})
    assert b'Post has no content' in response.data
    auth.logout()

    auth.login()
    response = response = client.get('/')
    assert b'empty title' not in response.data
    assert b'empty body' not in response.data

def test_subscribe(client, auth):
    auth.login()
    response = client.get('/users')
    assert b'Unsubscribe' in response.data
    response = client.post('/users', data={'sub':2})
    assert b'Subscribe' in response.data
    response = client.post('/users', data={'sub':2})
    assert b'Unsubscribe' in response.data
