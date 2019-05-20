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

def test_empty_dictionaries(client):
    """ Any empty environment should have no in built dictionaries    
    """
    response = client.get('/api/dictionary', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    assert len(response.json["names"]) == 0 

@pytest.mark.parametrize("name", ["01234567890123456789012345678901234567890", 
                                   "illegal_",
                                    "!noname",
                                    "illegal_/word"])
def test_invalid_dictionary_names(client, name):
    """ Create dictionaries of invalid names
    """
    response = client.post(f'/api/dictionary/{name}', 
            data='["one", "two", "three"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 400

    response = client.get(f'/api/dictionary/{name}', headers={'content-type': 'application/json'})
    assert response.status_code == 400

# curl -X POST "http://localhost:8000/api/dictionary/test" -d '["one", "two", "three"]' --header "content-type:application/json" ${VERBOSE}
def test_create_dictionary(client):
    """ Create a dictionary and check it exists
    """
    response = client.post('/api/dictionary/test', 
            data='["one", "two", "three"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.get('/api/dictionary', headers={'content-type': 'application/json'})
    assert response.status_code == 200
    assert len(response.json["names"]) == 1 

# curl -X GET "http://localhost:8000/api/dictionary/test" --header "content-type:application/json" ${VERBOSE}
def test_get_dictionary(client):
    """ Create a dictionary and ensure it has correct properties
    """
    response = client.post('/api/dictionary/test', 
            data='["one", "two"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201
    response = client.get('/api/dictionary/test', headers={'content-type': 'application/json'})
    assert response.json["id"] == "test"
    assert response.json["longest_word_length"] == 3
    assert response.json["num_of_words"] == 2

# curl -X PUT "http://localhost:8000/api/dictionary/test" -d '["wrwr", "wrwrw", "qweewe"]' --header "content-type:application/json" ${VERBOSE}
def test_add_dictionary(client):
    """ Create a populated dictionary, add a list of words to it and check properties are correct 
    """
    response = client.post('/api/dictionary/test', 
            data='["one", "two"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201
    response = client.get('/api/dictionary/test', 
            headers={'content-type': 'application/json'})
    assert response.json["id"] == "test"
    assert response.json["longest_word_length"] == 3
    assert response.json["num_of_words"] == 2

    # add words including repeats
    response = client.put('/api/dictionary/test', 
            data='["one", "two", "three", "four"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201
    response = client.get('/api/dictionary/test', 
            headers={'content-type': 'application/json'})
    assert response.json["id"] == "test"
    assert response.json["longest_word_length"] == 5
    assert response.json["num_of_words"] == 4

# curl -X PUT "http://localhost:8000/api/dictionary/test" -d "[$quoted]" --header "content-type:application/json" ${VERBOSE}
def test_add_single_word_dictionary(client):
    """ Create a populated dictionary, add a single word to it and check properties are correct 
    """
    response = client.post('/api/dictionary/test', 
            data='["one", "two"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.post('/api/dictionary/test/fifteen', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.get('/api/dictionary/test', 
            headers={'content-type': 'application/json'})
    assert response.json["id"] == "test"
    assert response.json["longest_word_length"] == 7
    assert response.json["num_of_words"] == 3


# curl -X GET "http://localhost:8000/api/dictionary/test/one" --header "content-type:application/json" ${VERBOSE}
def test_word_existence(client):
    """ Create a populated dictionary, test that words exist
    """
    response = client.post('/api/dictionary/test', 
            data='["one", "two"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.post('/api/dictionary/test/fifteen', headers={'content-type': 'application/json'})
    assert response.status_code == 201

    response = client.get('/api/dictionary/test', headers={'content-type': 'application/json'})
    assert response.json["id"] == "test"
    assert response.json["longest_word_length"] == 7
    assert response.json["num_of_words"] == 3

    response = client.get('/api/dictionary/test/fifteen', headers={'content-type': 'application/json'})
    assert response.status_code == 200

    response = client.get('/api/dictionary/test/sixteen', headers={'content-type': 'application/json'})
    assert response.status_code == 404


