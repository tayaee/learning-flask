from flaskr import create_app


# Test factory
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


# Test Web endpoint
def test_client(client):
    response = client.get('/hello')
    assert response.data == b'Hello World!'
