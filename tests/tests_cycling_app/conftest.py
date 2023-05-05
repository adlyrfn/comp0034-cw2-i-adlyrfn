import pytest
from cycling_app import create_app, config

@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing"""
    app = create_app(config.TestConfig)
    yield app


@pytest.fixture(scope="function")
def test_client(app):
    """ Flask test client within an application context. """
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client