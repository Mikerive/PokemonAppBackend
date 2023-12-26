from flask import Blueprint, jsonify, session, request
from dao.user_dao import UserDAO
from models.collection import MarketListing
from service.card_service import CardService
from service.user_service import UserService
from service.market_listing_service import MarketListingService

collection_bp = Blueprint('collection', __name__)


#https://pokemonappbackend.michaelrivera15.repl.co/collection
@collection_bp.route("/")
def collection():
  user_id = session.get('user_id')
  if not user_id:
    return jsonify({"message": "Unauthorized - User not logged in"}), 401

  card_service = CardService()
  card_data = card_service.get_user_collection(user_id)

  user_service = UserService()
  user_data = user_service.get_user(user_id)

  if 'error' in card_data:
    return jsonify(card_data), 400

  #Return the card data in the JSON response
  return jsonify({
      "message": "User collection retrieval successful",
      "data": card_data,
      "user": {
          "username": user_data.username,
          "email": user_data.email,
          "phone": user_data.phoneNumber,
      },
  }), 200
  #return card_data, 200


#https://pokemonappbackend.michaelrivera15.repl.co/collection/add
@collection_bp.route("/add", methods=['POST'])
def add_card():
  #Adding card to user's collection
  user_id = session.get('user_id')
  if not user_id:
    return jsonify({"message": "Unauthorized - User not logged in"}), 401

  data = request.json

  #Return error if card does not exist
  card_service = CardService()
  if not card_service.check_card_exist(data['card_id']):
    return jsonify({"message": "Card does not exist"}), 400

  qNum = CardService.add_card_to_user_collection(user_id, data['card_id'])
  return jsonify({"qNum": qNum})

#https://pokemonappbackend.michaelrivera15.repl.co/collection/view_selling
@collection_bp.route("/view_selling", methods=["GET"])
def view_selling():
  user_id = session.get('user_id')
  if not user_id:
    return jsonify({"message": "Unauthorized - User not logged in"}), 401

  market_listing_service = MarketListingService()
  listings = market_listing_service.get_all_user_listings(user_id)
  cards = [listing.to_dict() for listing in listings]

  return jsonify(cards)
  
#https://pokemonappbackend.michaelrivera15.repl.co/collection/cancel/<listing_id>
@collection_bp.route("/cancel/<int:listing_id>", methods=['DELETE'])
def cancel_listing(listing_id):
  #Delete listing, still keep in sellers collection
  MarketListingService.delete_listing(listing_id)
  return jsonify({"message": "Listing canceled"})


#https://pokemonappbackend.michaelrivera15.repl.co/collection/change_price/<int:listing_id>
@collection_bp.route("/change_price/<int:listing_id>", methods=['PUT'])
def change_price(listing_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized - User not logged in"}), 401

    data = request.json
    price = data.get('price')
    if not price or not isinstance(price, (int, float)):
        return jsonify({"message": "Invalid price"}), 400

    market_listing_service = MarketListingService()
    listing = market_listing_service.get_listing_details(listing_id)
    if not listing or listing.userID != user_id:
        return jsonify({"message": "Listing not found or unauthorized"}), 404

    # Update the price
    market_listing_service.update_listing(listing_id, {"price": price})
    return jsonify({"message": "Price updated successfully"}), 200


  #https://pokemonappbackend.michaelrivera15.repl.co/collection/change_quality/<int:listing_id>
@collection_bp.route("/change_quality/<int:listing_id>", methods=['PUT'])
def change_quality(listing_id):
    # Get the user ID from the session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized - User not logged in"}), 401

    # Get the quality data from the request
    data = request.json
    quality = data.get('quality')

    # Check if the quality is provided and is a valid value
    valid_qualities = ["Mint", "Near Mint", "Good", "Played", "Well Played"]
    if not quality or quality not in valid_qualities:
        return jsonify({"message": "Invalid quality"}), 400

    # Initialize the MarketListingService
    market_listing_service = MarketListingService()

    # Get the details of the listing
    listing = market_listing_service.get_listing_details(listing_id)

    # Check if the listing is found and belongs to the user
    if not listing or listing.userID != user_id:
        return jsonify({"message": "Listing not found or unauthorized"}), 404

    # Update the quality of the listing
    market_listing_service.update_listing(listing_id, {"quality": quality})

    return jsonify({"message": "Quality updated successfully"}), 200
