from models.user import User
from sqlalchemy import func


class UserDAO:

  def __init__(self, session):
    self.session = session

  def create_user(self, data):
    user = User(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        address=data.get('address',
                         ''),  # Using .get() in case some fields are optional
        phoneNumber=data.get('phoneNumber', ''),
        userRank=data.get('userRank',
                          0),  # Default rank can be 0 if not provided
        isActive=data.get('isActive', 'True'),
        userRole=data.get('userRole',
                          'User')  # Default role is 'User' if not provided
    )
    self.session.add(user)
    self.session.commit()
    return user.id

  def get_user_by_id(self, user_id):
    return self.session.query(User).get(user_id)

  def update_user(self, user_id, data):
    user = self.session.query(User).get(user_id)
    if not user:
      return None
    for key, value in data.items():
      if hasattr(user, key):
        setattr(user, key, value)
    self.session.commit()
    return user_id

  def delete_user(self, user_id):
    user = self.session.query(User).get(user_id)
    if user:
      self.session.delete(user)
      self.session.commit()
      return True
    return False

  def list_users(self, filter_condition=None):
    query = self.session.query(User)
    if filter_condition:
      query = query.filter(filter_condition)
    return query.all()

  def get_users_by_role(self, role):
    return self.session.query(User).filter(User.userRole == role).all()

  def get_users_by_rank_range(self, min_rank, max_rank):
    return self.session.query(User).filter(
        User.userRank.between(min_rank, max_rank)).all()

  def get_user_by_email(self, email):
    return self.session.query(User).filter(User.email == email).first()

  def get_user_by_phone_number(self, phone_number):
    return self.session.query(User).filter(
        User.phoneNumber == phone_number).first()

  def get_user_by_username(self, username):
    return self.session.query(User).filter(User.username == username).first()

  def get_random_user(self):
    random_user = self.session.query(User).order_by(func.random()).first()
    return random_user

  # Maintaining the original method names for clarity, using the dunder methods internally
