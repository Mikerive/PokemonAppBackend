import sqlalchemy
from sqlalchemy import Column, Integer, Boolean, Float, String
from .base import Base

Quality = sqlalchemy.Enum("Mint",
                          "Near Mint",
                          "Good",
                          "Played",
                          "Well Played",
                          name="quality")


class UserCardCollection(Base):
  __tablename__ = 'UserCardCollection'

  qNum = Column(Integer, primary_key=True, autoincrement=True)
  userID = Column(Integer)  # Sharded based on userID
  cardID = Column(String(50))
  for_sale = Column(Boolean, default=False)

  # User checks card sales from Collection, not from market listing


# We can create an identical CardCollection and shard the cardID if the need arises.


# Constitutes the market for each card.
class MarketListing(Base):
  __tablename__ = 'MarketListing'
  listing_id = Column(Integer, primary_key=True, autoincrement=True)
  userID = Column(Integer)
  cardID = Column(String(50))  # Sharded based on cardID
  picture = Column(String(255))  # URL or path to the picture
  price = Column(Float)  # Price of the card
  quality = Column(Quality, default="Near Mint")

  def to_dict(self):
    return {
        'listing_id': self.listing_id,
        'userID': self.userID,
        'cardID': self.cardID,
        'picture': self.picture,
        'price': self.price,
        'quality': self.quality,
        # Include other attributes as needed
    }
