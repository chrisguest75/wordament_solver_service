import pytest
import connexion
from state_manager_factory import state_manager_factory, injector_factory

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('./openapi/service_api.yaml')
flask_app.testing = True


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def setup_test():
    injector_factory.configure(True)  


def test_health(client):
    """ Test health endpoint returns 200    
    """
    response = client.get('/api/health')
    assert response.status_code == 200


def test_health_with_multiple_dictionaries(client):
    """ Create a dictionary and check it exists
    """
    response = client.post('/api/dictionary/test', 
            data='["one", "two", "three"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.post('/api/dictionary/test2', 
            data='["four", "five", "six"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.get('/api/dictionary', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    assert len(response.json["names"]) == 2 

    response = client.get('/api/dictionary/test/one', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    response = client.get('/api/dictionary/test/two', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    response = client.get('/api/dictionary/test/three', headers={'content-type': 'application/json'})
    assert response.status_code == 200

    response = client.get('/api/dictionary/test2/four', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    response = client.get('/api/dictionary/test2/five', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    response = client.get('/api/dictionary/test2/six', headers={'content-type': 'application/json'})
    assert response.status_code == 200

    response = client.get('/api/health')
    assert response.status_code == 200
    assert len(response.json['dictionaries'].keys()) == 2 
    assert response.json['dictionaries']['test']['longest_word_length'] == 5 
    assert response.json['dictionaries']['test']['num_of_words'] == 3 
    assert response.json['dictionaries']['test2']['longest_word_length'] == 4 
    assert response.json['dictionaries']['test2']['num_of_words'] == 3 
