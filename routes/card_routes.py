from flask import Blueprint, jsonify, request
from service.card_service import CardService

#https://pokemonappbackend.michaelrivera15.repl.co/card
card_bp = Blueprint('card', __name__)


#https://pokemonappbackend.michaelrivera15.repl.co/card/search
@card_bp.route('/search', methods=['GET'])
def get_card():
  input_str = request.args.get('input', default='', type=str)
  if not input_str:
    return jsonify({'error': 'No input provided'}), 400

  try:
    card_details = CardService.get_card_details_by_user_input(input_str)
    return jsonify(card_details)
  except Exception as e:
    return jsonify({'error': str(e)}), 500
