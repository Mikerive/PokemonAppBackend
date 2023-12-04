from bcrypt import hashpw, gensalt, checkpw
from dao.user_dao import UserDAO
from models.user import User
from database.engine import DatabaseEngine
import re


class UserService:

  @staticmethod
  def _get_session():
    """Get a new database session."""
    return DatabaseEngine().get_session()

  @staticmethod
  def _hash_password(password):
    hashed = hashpw(password.encode('utf-8'), gensalt())
    return hashed.decode('utf-8')

  @staticmethod
  def _verify_password(stored_password, provided_password):
    return checkpw(provided_password.encode('utf-8'),
                   stored_password.encode('utf-8'))

  @staticmethod
  def is_valid_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None

  @staticmethod
  def is_valid_phone_number(phone_number):
    #phone_regex = r"^\+?\d{10,15}$"
    phone_regex = r"^\+?[\dx().-]{10,30}$" #Faker phone_number
    return re.match(phone_regex, phone_number) is not None

  @staticmethod
  def is_valid_password(password):
    password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$"
    return re.match(password_regex, password) is not None

  @staticmethod
  def create_user(data):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    # Data validation
    if not UserService.is_valid_email(data['email']):
      session.close()
      return {'error': 'Invalid email format.'}
    if 'phoneNumber' in data and not UserService.is_valid_phone_number(
        data['phoneNumber']):
      session.close()
      return {'error': 'Invalid phone number format.'}

    if 'password' in data and not UserService.is_valid_password(
        data['password']):
      session.close()
      return {
          'error':
          'At least 8 characters, one Uppercase character, and one special character !@#$%^&*'
      }

    # Check for existing data
    if user_dao.get_user_by_username(data['username']):
      session.close()
      return {'error': 'Username already exists.'}
    if user_dao.get_user_by_email(data['email']):
      session.close()
      return {'error': 'Email already exists.'}
    if 'phoneNumber' in data and user_dao.get_user_by_phone_number(
        data['phoneNumber']):
      session.close()
      return {'error': 'Phone number already exists.'}

    # Hash password and create user
    data['password'] = UserService._hash_password(data['password'])
    user_id = user_dao.create_user(data)
    session.close()
    return {'success': 'User created successfully.', 'user_id': user_id}

  @staticmethod
  def login(identifier, password):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    user = None
    if UserService.is_valid_email(identifier):
      user = user_dao.get_user_by_email(identifier)
    elif UserService.is_valid_phone_number(identifier):
      user = user_dao.get_user_by_phone_number(identifier)
    else:
      user = user_dao.get_user_by_username(identifier)

    if not user:
      session.close()
      return {'error': 'Identifier not found.'}

    if not UserService._verify_password(user.password, password):
      session.close()
      return {'error': 'Incorrect password.'}

    session.close()
    return {'success': 'Login successful.', 'user_id': user.id}

  @staticmethod
  def get_user(user_id):
    session = UserService._get_session()
    user_dao = UserDAO(session)
    user = user_dao.get_user_by_id(user_id)
    session.close()
    return user

  @staticmethod
  def update_user(user_id, data):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    if 'password' in data:
      data['password'] = UserService._hash_password(data['password'])

    result = user_dao.update_user(user_id, data)
    session.close()
    return result

  @staticmethod
  def delete_user(user_id):
    session = UserService._get_session()
    user_dao = UserDAO(session)
    result = user_dao.delete_user(user_id)
    session.close()
    return result

  @staticmethod
  def list_users():
    session = UserService._get_session()
    user_dao = UserDAO(session)
    users = user_dao.list_users()
    session.close()
    return users

  @staticmethod
  def authenticate(username, password):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    user = user_dao.get_user_by_username(username)
    if not user or not UserService._verify_password(user.password, password):
      session.close()
      return None

    session.close()
    return user

  @staticmethod
  def has_role(user_id, role):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    user = user_dao.get_user_by_id(user_id)
    result = user.userRole == role if user else False

    session.close()
    return result

  @staticmethod
  def change_password(user_id, old_password, new_password):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    user = user_dao.get_user_by_id(user_id)
    if not user or not UserService._verify_password(user.password,
                                                    old_password):
      session.close()
      return False

    user_dao.update_user(
        user_id, {"password": UserService._hash_password(new_password)})

    session.close()
    return True

  @staticmethod
  def activate_user(user_id):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    result = user_dao.update_user(user_id, {"isActive": True})

    session.close()
    return result

  @staticmethod
  def deactivate_user(user_id):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    result = user_dao.update_user(user_id, {"isActive": False})

    session.close()
    return result

  @staticmethod
  def is_active(user_id):
    session = UserService._get_session()
    user_dao = UserDAO(session)

    user = user_dao.get_user_by_id(user_id)
    result = user.isActive if user else False

    session.close()
    return result

  @staticmethod
  def log_activity(user_id, activity):
    # Just a simple print for now
    print(f"Logged activity for user {user_id}: {activity}")

  @staticmethod
  def get_activity_logs(user_id):
    # Return a sample log for now
    return [f"Sample activity log for user {user_id}"]

  @staticmethod
  def send_notification(user_id, message):
    # Just a simple print for now
    print(f"Sent notification to user {user_id}: {message}")
