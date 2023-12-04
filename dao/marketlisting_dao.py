from models.collection import MarketListing


class MarketListingDAO:

  def __init__(self, session):
    self.session = session

  def new_listing(self, user_id, card_id, picture, price, quality):
    new_listing = MarketListing(userID=user_id,
                                cardID=card_id,
                                picture=picture,
                                price=price,
                                quality=quality)
    self.session.add(new_listing)
    self.session.commit()
    return new_listing.listing_id

  def get_all_listings(self):
    return self.session.query(MarketListing).all()

  def get_listing_by_id(self, id):
    return self.session.query(MarketListing).filter_by(listing_id=id).first()

  def update_listing(self, qNum, data):
    listing = self.session.query(MarketListing).filter_by(qNum=qNum).first()
    if listing:
      for key, value in data.items():
        if hasattr(listing, key):
          setattr(listing, key, value)
      self.session.commit()

  def delete_listing(self, qNum):
    listing = self.session.query(MarketListing).filter_by(qNum=qNum).first()
    if listing:
      self.session.delete(listing)
      self.session.commit()

  def query_equal_price(self, price):
    return self.session.query(MarketListing).filter(
        MarketListing.price == price).all()

  def query_lessthan_price(self, price):
    return self.session.query(MarketListing).filter(
        MarketListing.price < price).all()

  def query_greaterthan_price(self, price):
    return self.session.query(MarketListing).filter(
        MarketListing.price > price).all()

  def query_quality(self, quality):
    return self.session.query(MarketListing).filter(
        MarketListing.quality == quality).all()
