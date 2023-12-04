import json
import pytest
from flask import Flask
from routes.card_routes import card_bp
from service.card_service import CardService


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(card_bp, url_prefix='/card')
    app.secret_key = '7103a98b1a7555d73e40990b'
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_card_route(client, monkeypatch):  # Add monkeypatch as a parameter here
    # Define a sample card input
    input_str = "pikachu"

    # Mock the CardService to return a predefined result
    def mock_get_card_details_by_user_input(input_str):
        # Return a sample card details response
        return {'name': 'Sample Card', 'type': 'Fire', 'hp': 100}

    # Replace the original CardService method with the mock
    monkeypatch.setattr(CardService, 'get_card_details_by_user_input', mock_get_card_details_by_user_input)

    # Make a GET request to the search route
    response = client.get(f'/card/search?input={input_str}')

    # Validate the response
    assert response.status_code == 200  # Check if the status code is correct

    # Validate the content of the response
    expected_response = {'name': 'Sample Card', 'type': 'Fire', 'hp': 100}
    assert json.loads(response.data) == expected_response
