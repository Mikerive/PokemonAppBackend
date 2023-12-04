from sqlalchemy import Column, Integer, String, Enum
from .base import Base


class User(Base):
  __tablename__ = 'Users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(100), unique=True)
  password = Column(String(100))
  email = Column(String(100), unique=True)
  address = Column(String(100))
  phoneNumber = Column(String(100))
  isActive = Column(Enum('True', 'False'), default='True')
  userRank = Column(Integer)
  userRole = Column(Enum('Admin', 'Owner', 'User'))
