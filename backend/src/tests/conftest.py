import pytest
from main import create_app

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    """Test client for making requests."""
    return app.test_client()