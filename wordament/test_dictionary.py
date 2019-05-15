import pytest
import connexion

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('./openapi/service_api.yaml')
flask_app.testing = True

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c

def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200

# curl -X POST "http://localhost:8000/api/dictionary/test" -d '["one", "two", "three"]' --header "content-type:application/json" ${VERBOSE}
def test_create_dictionary(client):
    response = client.post('/api/dictionary/test', 
            data='["one", "two", "three"]', 
            headers={'content-type': 'application/json'})
    assert response.status_code == 201





# curl -X GET "http://localhost:8000/api/dictionary/test" --header "content-type:application/json" ${VERBOSE}

# curl -X PUT "http://localhost:8000/api/dictionary/test" -d '["wrwr", "wrwrw", "qweewe"]' --header "content-type:application/json" ${VERBOSE}

# curl -X GET "http://localhost:8000/api/dictionary/test" --header "content-type:application/json" ${VERBOSE}

# read -p "Enter word to add to dictionary: " NUMBER
# echo "Add $NUMBER"
# quoted="\"$NUMBER\""

# curl -X PUT "http://localhost:8000/api/dictionary/test" -d "[$quoted]" --header "content-type:application/json" ${VERBOSE}

# curl -X GET "http://localhost:8000/api/dictionary/test" --header "content-type:application/json" ${VERBOSE}

# curl -X GET "http://localhost:8000/api/dictionary/test/one" --header "content-type:application/json" ${VERBOSE}
# curl -X GET "http://localhost:8000/api/dictionary/test/four" --header "content-type:application/json" ${VERBOSE}

# curl -X POST "http://localhost:8000/api/dictionary/test/up${NUMBER}" ${VERBOSE}
# curl -X GET "http://localhost:8000/api/dictionary/test/up${NUMBER}" ${VERBOSE}
