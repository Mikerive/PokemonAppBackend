from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP, Enum, DECIMAL, String
import json
from .base import Base


class MarketTransactions(Base):
  __tablename__ = 'MarketTransactions'
  transactionID = Column(Integer, primary_key=True, autoincrement=True)
  UserID = Column(Integer)  # sharded based on UserID - users need to get their info faster than admins
  cards_data = Column(
      String(3000))  # This will store the serialized list of dictionaries
  transactionTimestamp = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
  transactionStatus = Column(Enum('Pending', 'Completed', 'Canceled'),
                             default='Pending')
  transactionPrice = Column(DECIMAL(10, 2))

  @property
  def cards(self):
    return json.loads(self.cards_data)

  @cards.setter
  def cards(self, cards_list):
    self.cards_data = json.dumps(cards_list)
