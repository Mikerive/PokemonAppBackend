from service.market_listing_service import MarketListingService
from flask import Blueprint, jsonify, request, session
import traceback
import logging

cart_bp = Blueprint('cart', __name__)

# If there are two of the same card on the cart, it should be able to add the quantity and represent it as card picture, card name, cart quantity.


# Add listing to cart - support for duplicate listings - takes listing id as post input
# https://pokemonappbackend.michaelrivera15.repl.co/cart/add_to_cart
@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
  listing_id = request.json.get('listing_id')
  if not listing_id:
    return jsonify({"error": "Listing ID is required"}), 400

  listing = MarketListingService.get_listing_details(listing_id)
  if not listing:
    return jsonify({"error": "Listing not found"}), 404

  if 'cart' not in session:
    session['cart'] = []

  # Check if the item is already in the cart and update quantity
  cart_item = next(
      (item for item in session['cart'] if item['listing_id'] == listing_id),
      None)
  if cart_item:
    # If the item is found, increment the quantity
    cart_item['quantity'] += 1
  else:
    # If the item is not found, add it with a quantity of 1
    session['cart'].append({
        'card_id': listing.cardID,
        'listing_id': listing_id,
        'image_url': listing.picture,
        'price': listing.price,
        'quantity': 1  # Start with a quantity of 1
    })

  session.modified = True
  return jsonify({"success": "Added to cart"}), 200


# Takes card id as post input and calls market_listing_from_card to create the market listing - takes card_id as input
# https://pokemonappbackend.michaelrivera15.repl.co/cart/make_fake_listing
@cart_bp.route('/make_fake_listing', methods=['POST'])
def make_fake_listing():
  try:
    # Retrieve card ID from the POST request
    data = request.get_json()
    logging.debug(f"Received data: {data}")  # Log the received data

    card_id = data.get('card_id')

    # Validate that card ID is provided
    if not card_id:
      return jsonify({"error": "Card ID is required"}), 400

    # Call the function to create a market listing
    listing_id = MarketListingService.create_market_listing_from_card(card_id)
    return jsonify({
        "success": "Market listing created",
        "listing_id": listing_id
    }), 200
  except Exception as e:
    # Detailed error logging
    logging.error(f"Error occurred: {e}")
    traceback.print_exc()  # Print stack trace for detailed debugging

    # Return a generic error message to the client
    return jsonify({"error": "An internal error occurred"}), 500


# https://pokemonappbackend.michaelrivera15.repl.co/cart/view_cart
@cart_bp.route('/view_cart', methods=['GET'])
def view_cart():
  if 'cart' in session and session['cart']:
    return jsonify({"cart": session['cart']}), 200
  else:
    print("empty")
    return jsonify({"cart": []}), 200


# Remove listing from cart - if there is a duplicate listing, then remove the more expensive one.
# https://pokemonappbackend.michaelrivera15.repl.co/cart/remove_from_cart
@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
  card_id = request.json.get('card_id')
  if not card_id:
    return jsonify({"error": "Card ID is required"}), 400

  if 'cart' not in session or not session['cart']:
    return jsonify({"error": "Cart is empty"}), 400

  # Find the first item with the given card_id
  item_to_remove = next(
      (item for item in session['cart'] if item['card_id'] == card_id), None)

  if item_to_remove:
    session['cart'].remove(item_to_remove)
    session.modified = True
    return jsonify({"success": "Removed from cart"}), 200
  else:
    return jsonify({"error": "Item not found in cart"}), 404


# Empty the cart
# https://pokemonappbackend.michaelrivera15.repl.co/cart/empty_cart
@cart_bp.route('/empty_cart', methods=['POST'])
def empty_cart():
  if 'cart' in session:
    session['cart'] = []
    session.modified = True
    return jsonify({"success": "Cart emptied"}), 200
  else:
    return jsonify({"error": "Cart is already empty"}), 400
