from flask import Blueprint, jsonify, request, session
from service.market_listing_service import MarketListingService

#https://pokemonappbackend.michaelrivera15.repl.co/market
market_bp = Blueprint('market', __name__)

# # Default - Display all cards for sale
# @market.route("/")
# def market():
#   #listings = MarketListingService.get_all_market_listings()
#   listings = MarketListingService.get_all_market_listings_with_card_details()

#   return jsonify({
#       "message": "Market Listings retrieval successful",
#       "data": listings,
#   }), 200


#https://pokemonappbackend.michaelrivera15.repl.co/market/<card_id>
@market_bp.route("/<card_id>")
def list_all_market_listings_by_card(card_id):
  listings = MarketListingService.list_all_market_listings_by_card(card_id)
  return jsonify(listings)


#https://pokemonappbackend.michaelrivera15.repl.co/market/add
@market_bp.route("/add", methods=['POST'])
def add_new_listing():
  user_id = session.get('user_id')
  data = request.json
  qNum = MarketListingService.add_new_listing(user_id, data['card_id'],
                                              data['picture'], data['price'],
                                              data['quality'])
  return jsonify({"qNum": qNum})


#https://pokemonappbackend.michaelrivera15.repl.co/market/add_fake
@market_bp.route("/add_fake", methods=['POST'])
def add_fake_listing():
  user_id = session.get('user_id')
  data = request.json
  qNum = MarketListingService.create_market_listing_from_card(
      user_id, data['card_id'], data['picture'], data['price'],
      data['quality'])
  return jsonify({"qNum": qNum})


#https://pokemonappbackend.michaelrivera15.repl.co/market/details/<card_id>/<qNum>
@market_bp.route("/details/<card_id>/<int:qNum>")
def get_listing_details(card_id, qNum):
  listing = MarketListingService.get_listing_details(card_id, qNum)
  return jsonify(listing)


#https://pokemonappbackend.michaelrivera15.repl.co/market/delete/<card_id>/<qNum>
@market_bp.route("/delete/<card_id>/<int:qNum>", methods=['DELETE'])
def delete_listing(card_id, qNum):
  MarketListingService.delete_listing(card_id, qNum)
  return jsonify({"message": "Listing deleted"})


#https://pokemonappbackend.michaelrivera15.repl.co/market/price-less/<card_id>/<price>
@market_bp.route("/price-less/<card_id>/<float:price>")
def get_listings_by_lessthan_price(card_id, price):
  listings = MarketListingService.get_listings_by_lessthan_price(
      card_id, price)
  return jsonify(listings)
