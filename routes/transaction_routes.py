from flask import Blueprint, jsonify, request, session
from service.market_transaction_service import MarketTransactionService

transaction_bp = Blueprint('transaction', __name__)


# Finish Transaction - Buy the Cart of Cards
@transaction_bp.route('/finish_transaction', methods=['POST'])
def finish_transaction():
  # Ensure there is a cart in the session
  if 'cart' not in session or not session['cart']:
    return jsonify({"error": "Cart is empty"}), 400

  user_id = session.get(
      'user_id'
  )  # Retrieve user ID from session, adjust based on your session management
  if not user_id:
    return jsonify({"error": "User not identified"}), 401

  try:
    # Retrieve cart items from the session
    cart_items = session['cart']

    # Create a transaction using the MarketTransactionService
    transaction_id = MarketTransactionService.create_transaction(
        user_id=user_id, listings=cart_items)

    # Clear the cart after successful transaction
    session['cart'] = []
    session.modified = True

    return jsonify({
        "success": "Transaction completed",
        "transaction_id": transaction_id
    }), 200

  except Exception as e:
    # Handle exceptions and errors
    return jsonify({"error": str(e)}), 500
