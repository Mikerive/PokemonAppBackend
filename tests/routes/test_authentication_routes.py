import json
import pytest
from flask import Flask
from faker import Faker
from routes.authentication_routes import auth_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.secret_key = '7103a98b1a7555d73e40990b'
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def generate_fake_user_data():
  fake = Faker()
  unique_username = fake.user_name()
  #unique_password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
  unique_password = 'Abcdefg123!'
  unique_email = fake.email()
  unique_phone_number = fake.phone_number()
  user_data = {
      'username': unique_username,
      'password': unique_password,
      'email': unique_email,
      'phoneNumber': unique_phone_number
  }
  return user_data


def test_succesful_register_login_route(client):
    # Generate unique user data
    user_data = generate_fake_user_data()
    
    # Make a POST request to the register route
    response = client.post('/auth/register', json=user_data)
    print(response.data)
    # Validate the response
    assert response.status_code == 201
    assert b'Registration successful' in response.data

    login_data = {
      'username': user_data['username'],
      'password': user_data['password']
    }
    login_response = client.post('/auth/login', json=login_data)
    assert login_response.status_code == 200
    assert b'Login successful' in login_response.data
