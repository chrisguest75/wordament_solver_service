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

def test_solve_puzzle_illegal_dictionary_name(client):
    """ Invoke solve with an illegal dictionary name
    """
    response = client.get('/api/puzzle/solve/GLNTSRAWRPHSEOPS?dictionary_id=01234567890123456789012345678901234567890', headers={'content-type': 'application/json'})
    assert response.status_code == 500


def test_solve_puzzle_missing_dictionary(client):
    """ Invoke solve with a dictionary name that does not exist.
    """
    response = client.get('/api/puzzle/solve/GLNTSRAWRPHSEOPS?dictionary_id=puzzle1', headers={'content-type': 'application/json'})
    assert response.status_code == 500

def test_solve_simple_puzzle(client):
    """ Create a dictionary and check it exists
    """
    response = client.post('/api/dictionary/puzzle1', 
            data='["like", "shops", "shop", "wasp", "want", "hops"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.get('/api/dictionary', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    assert len(response.json["names"]) == 1 

    response = client.get('/api/puzzle/solve/GLNTSRAWRPHSEOPS?dictionary_id=puzzle1', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    assert len(response.json["words"]) == 5 
    assert "shops" in response.json["words"]
    assert "shop" in response.json["words"]
    assert "wasp" in response.json["words"]
    assert "want" in response.json["words"]
    assert "hops" in response.json["words"]


