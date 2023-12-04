from dao.card_dao import CardDAO
from database.engine import DatabaseEngine
from typing import List, Optional
from models.card import Card
import json
from dao.collection_dao import UserCardCollectionDAO


class CardService:

  @staticmethod
  def get_session():
    """Create and return a new session."""
    return DatabaseEngine.get_session()

  @staticmethod
  def close_session(session):
    """Close the provided session."""
    session.close()

  @staticmethod
  def get_card_details_from_card(card: Card) -> dict:
    # Extract TCG Player Prices
    tcg_player_prices = None
    if hasattr(
        card, 'tcgplayer'
    ) and 'prices' in card.tcgplayer and 'holofoil' in card.tcgplayer['prices']:
      tcg_player_prices = card.tcgplayer['prices']['holofoil']['market']

    # Extract Images
    image_instance = getattr(card, 'images', {})
    small_image_url = image_instance.get('small') if image_instance else None
    large_image_url = image_instance.get('large') if image_instance else None

    # Parse Set Information
    set_name = None
    if hasattr(card, 'set'):
      set_attr = card.set
      if isinstance(set_attr, str):
        try:
          set_name = json.loads(set_attr).get('name')
        except json.JSONDecodeError:
          pass
      elif isinstance(set_attr, dict):
        set_name = set_attr.get('name')

    # Construct Card Details Dictionary
    card_detail = {
        "id": getattr(card, 'id', None),
        "name": getattr(card, 'name', None),
        "price": tcg_player_prices,
        "rarity": getattr(card, 'rarity', None),
        "small_image_url": small_image_url,
        "large_image_url": large_image_url,
        "artist": getattr(card, 'artist', None),
        "flavor_text": getattr(card, 'flavor_text', None),
        "national_pokedex_numbers": getattr(card, 'national_pokedex_numbers',
                                            None),
        "hp": getattr(card, 'hp', None),
        "supertype": getattr(card, 'supertype', None),
        "level": getattr(card, 'level', None),
        "set": set_name,
    }

    return card_detail

  @staticmethod
  def get_card_details_from_cards(cards: List[Card]) -> List[dict]:
    card_details = []
    for card in cards:
      tcg_player_prices = None
      tcgplayer_attr = getattr(card, 'tcgplayer', None)
      if tcgplayer_attr and 'prices' in tcgplayer_attr and 'holofoil' in tcgplayer_attr[
          'prices']:
        tcg_player_prices = tcgplayer_attr['prices']['holofoil']['market']

      image_instance = getattr(card, 'images', {})
      small_image_url = image_instance.get('small') if image_instance else None
      large_image_url = image_instance.get('large') if image_instance else None

      # Safe extraction of 'set' attribute and JSON parsing
      set_name = None
      # Handle the 'set' attribute
      set_attr = getattr(card, 'set', '{}')
      if isinstance(set_attr, str):
        try:
          set_name = json.loads(set_attr).get('name')
        except json.JSONDecodeError:
          set_name = None
      elif isinstance(set_attr, dict):
        set_name = set_attr.get('name')
      else:
        set_name = None

      card_detail = {
          "id":
          getattr(card, 'id', None),
          "name":
          getattr(card, 'name', None),
          "price":
          tcg_player_prices,
          "rarity":
          getattr(card, 'rarity', None),
          "small_image_url":
          small_image_url,
          "large_image_url":
          large_image_url,
          'artist':
          getattr(card, 'artist', None),
          'flavor_text':
          getattr(card, 'flavor_text', None),
          'national_pokedex_numbers':
          getattr(card, 'national_pokedex_numbers', None),
          'hp':
          getattr(card, 'hp', None),
          'supertype':
          getattr(card, 'supertype', None),
          'level':
          getattr(card, 'level', None),
          'set':
          set_name,
      }
      card_details.append(card_detail)

    return card_details

  @staticmethod
  def get_card_details_by_user_input(input_str: str) -> List[dict]:
    """
      Fetch the image URL, card name, and card price for a list of cards from a user query.
      """
    session = CardService.get_session()
    card_dao = CardDAO(session)
    cards = card_dao.get_cards_by_name(input_str)
    card_details = CardService.get_card_details_from_cards(cards)
    session.close()
    return card_details

  @staticmethod
  def get_user_collection(user_id: int) -> List[dict]:
    session = CardService.get_session()
    collection_dao = UserCardCollectionDAO(session)
    cards = collection_dao.get_cards_from_collection(user_id)
    card_details = CardService.get_card_details_from_cards(cards)
    session.close()
    return card_details

  @staticmethod
  def add_card_to_user_collection(user_id: int, card_id: str):
    session = CardService.get_session()
    collection_dao = UserCardCollectionDAO(session)
    collection_dao.add_card_to_collection(user_id, card_id)
    session.close()

  @staticmethod
  def check_card_exist(card_id: str):
    session = CardService.get_session()
    card_dao = CardDAO(session)
    card = card_dao.get_card_by_id(card_id)
    session.close()
    return False if card is None else True
