from flask import jsonify
from dao.marketlisting_dao import MarketListingDAO
from dao.card_dao import CardDAO
from dao.user_dao import UserDAO
from service.card_service import CardService
from database.engine import DatabaseEngine
from models.collection import MarketListing
from typing import List, Dict
import numpy as np


class MarketListingService:

  @staticmethod
  def create_market_listing_from_card(card_id: int):
    session = DatabaseEngine.get_session()
    # Get the market price from the card details
    card = CardDAO(session).get_card_by_id(card_id)
    card_details = CardService.get_card_details_from_card(card)
    market_price = card_details.get('price')
    if market_price is None:
      raise ValueError("Market price not available for the selected card")

    # Generate a new price based on normal distribution around the market price
    # Assuming a relatively tight distribution (e.g., standard deviation is 5% of the market price)
    std_dev = 0.05 * market_price
    new_price = np.random.normal(market_price, std_dev)

    # Ensure the new price is not negative
    new_price = max(new_price, 0)

    user_id = UserDAO(session).get_random_user().id

    # Extract other necessary details from the card detail
    card_id = card_details.get('id')
    if card_id is None:
      raise ValueError("Card ID not found in card details")

    small_image_url = card_details.get('small_image_url')

    # Assuming quality is a required detail for listing
    quality = "Good"  # Adjust as necessary

    session = DatabaseEngine().get_session()

    # Call the function to create a new market listing
    listing = MarketListingDAO(session).new_listing(user_id, card_id,
                                                    small_image_url, new_price,
                                                    quality)

    session.close()
    return listing

  @staticmethod
  def list_all_market_listings_by_card(card_id):
    session = DatabaseEngine().get_session()
    listings = session.query(MarketListing).filter_by(cardID=card_id).all()
    session.close()
    return listings

  @staticmethod
  def add_new_listing(user_id, card_id, picture, price, quality):
    session = DatabaseEngine().get_session()
    marketListingDAO = MarketListingDAO(session)
    listing_id = marketListingDAO.new_listing(user_id, card_id, picture, price,
                                              quality)
    session.close()
    return listing_id

  @staticmethod
  def get_listing_details(listing_id):
    session = DatabaseEngine().get_session()
    listing = MarketListingDAO(session).get_listing_by_id(listing_id)
    session.close()
    return listing

  @staticmethod
  def update_listing(listing_id, data):
    session = DatabaseEngine().get_session()
    listing = MarketListingService.get_listing_details(listing_id)
    if listing:
      for key, value in data.items():
        setattr(listing, key, value)
      session.commit()
    session.close()

  @staticmethod
  def delete_listing(listing_id):
    session = DatabaseEngine().get_session()
    listing = MarketListingService.get_listing_details(listing_id)
    if listing:
      session.delete(listing)
      session.commit()
    session.close()

  @staticmethod
  def get_listings_by_lessthan_price(card_id, price):
    session = DatabaseEngine().get_session()
    listings = session.query(MarketListing).filter(
        MarketListing.cardID == card_id, MarketListing.price < price).all()
    session.close()
    return listings

  @staticmethod
  def get_listings_by_greaterthan_price(card_id, price):
    session = DatabaseEngine().get_session()
    listings = session.query(MarketListing).filter(
        MarketListing.cardID == card_id, MarketListing.price > price).all()
    session.close()
    return listings

  @staticmethod
  def get_listings_by_quality(card_id, quality_enum):
    session = DatabaseEngine().get_session()
    listings = session.query(MarketListing).filter_by(
        cardID=card_id, quality=quality_enum).all()
    session.close()
    return listings

  # @staticmethod
  # def get_listings_by_user_and_card(user_id, card_id):
  #   session = DatabaseEngine().get_session()
  #   listings = session.query(MarketListing).filter_by(userID=user_id,
  #                                                     cardID=card_id).all()
  #   session.close()
  #   return listings
