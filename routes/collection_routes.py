from flask import Blueprint, jsonify, session, request
from dao.user_dao import UserDAO
from service.card_service import CardService
from service.user_service import UserService

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
