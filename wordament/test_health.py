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