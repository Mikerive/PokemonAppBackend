from flask import Blueprint, jsonify, request, session
from service.user_service import UserService
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)


#https://pokemonappbackend.michaelrivera15.repl.co/auth/register
@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  result = UserService.create_user(data)
  if 'error' in result:
    return jsonify(result), 400

  # Assuming result contains the user ID or some unique identifier
  user_id = result.get('user_id')
  if user_id:
    session[
        'user_id'] = user_id  # Start a session for the newly registered user
    return jsonify({"message": "Registration successful"}), 201
  else:
    # Handle the case where user ID is not returned
    return jsonify({"error": "Registration failed"}), 500


#https://pokemonappbackend.michaelrivera15.repl.co/auth/login
@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  user = UserService.authenticate(data['username'], data['password'])
  if not user:
    return jsonify({"msg": "Bad username or password"}), 401

  # Assuming `user` has an attribute `id` or similar unique identifier
  session['user_id'] = user.id  # Create a session for the authenticated user

  return jsonify({"message": "Login successful"}), 200
