import json
import pytest
from flask import Flask, session
from routes.cart_routes import cart_bp
from service.market_listing_service import MarketListingService


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.secret_key = '7103a98b1a7555d73e40990b'
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


def test_make_fake_listing_route(client):
    # Define a sample card ID
    card_id = 'base1-1'

    # Make a POST request to the make_fake_listing route
    response = client.post('/cart/make_fake_listing', json={'card_id': card_id})

    # Validate the response
    assert response.status_code == 200
    assert b'Market listing created' in response.data


def test_view_cart_route(client, app):
    # Make a GET request to the view_cart route
    response = client.get('/cart/view_cart')

    # Validate the response
    assert response.status_code == 200
    assert b'cart' in response.data


def test_add_to_cart_route(client, app):
    # Now, make a POST request to the add_to_cart route
    response = client.post('/cart/add_to_cart', json={'listing_id': 1})
    assert response.status_code == 200
    assert b'Added to cart' in response.data


# # def test_remove_from_cart_route(client, app):
# #   # Use test_request_context to work within a request context
# #   with app.test_request_context('/'):
# #       # Add cards to the cart for testing
# #       session['cart'] = [
# #           {'card_id': 'base4-4', 'quantity': 1},
# #           {'card_id': 'base1-1', 'quantity': 1}
# #       ]

# #       # Make a POST request to the remove_from_cart route
# #       response = client.post('/cart/remove_from_cart', json={'card_id': 'base4-4'})

# #       # Validate the response
# #       assert response.status_code == 200  # Expect 200 for successful removal
# #       assert b'Removed from cart' in response.data  # Adjust the success message as needed

#       # Check if the remaining card is still in the cart
#       assert 'cart' in session
#       assert len(session['cart']) == 1
#       assert session['cart'][0]['card_id'] == 'base1-1'
#       assert session['cart'][0]['quantity'] == 1



def test_empty_cart_route(client, app):
  with app.test_request_context('/'):
      session.clear()

  # Make a POST request to the empty_cart route
  response = client.post('/cart/empty_cart')

  # Validate the response
  assert response.status_code == 400  # Corrected to 400 if the cart is already empty
  assert b'Cart is already empty' in response.data  # Adjust the error message as needed