from models.card import Card
from typing import Optional, List
from sqlalchemy import or_


class CardDAO:

  def __init__(self, session):
    self.session = session

  def create_card(self, data):

    # Create the Card model
    card = Card(
        id=data.get('id', ''),
        name=data.get('name', ''),
        supertype=data.get('supertype', ''),
        subtypes=data.get('subtypes', []),
        level=data.get('level', 0),
        hp=data.get('hp', 0),
        types=data.get('types', []),
        evolves_from=data.get('evolvesFrom', ''),
        evolves_to=data.get('evolvesTo', []),
        rules=data.get('rules', []),
        ancientTrait=data.get('ancientTrait', {}),
        abilities=data.get('abilities', []),
        attacks=data.get('attacks', []),
        weaknesses=data.get('weaknesses', []),
        resistances=data.get('resistances', []),
        retreat_cost=data.get('retreatCost', []),
        converted_retreat_cost=data.get('convertedRetreatCost', 0),
        set=data.get('set', {}),
        number=data.get('number', ''),
        artist=data.get('artist', ''),
        rarity=data.get('rarity', ''),
        flavor_text=data.get('flavorText', ''),
        national_pokedex_numbers=data.get('nationalPokedexNumbers', []),
        legalities=data.get('legalities', {}),
        regulationMark=data.get('regulationMark', ''),
        images=data.get('images', {}),
        tcgplayer=data.get('tcgplayer', {}),
        cardmarket=data.get('cardmarket', {}),
    )

    try:
      self.session.add(card)
      self.session.commit()
      return card
    except Exception as e:
      self.session.rollback()
      raise e

  def get_id_by_name(self, cardName: str) -> Optional[str]:
    card_id = self.session.query(Card.id).filter_by(name=cardName).first()
    return card_id[0] if card_id else None

  def update_by_id(self, cardID: str, card: Card):
    existing_card = self.session.query(Card).filter_by(id=cardID).first()
    if existing_card:
      # Assuming you have a method or property to update the attributes of the card
      existing_card.update(card)
      self.session.commit()

  def delete_by_id(self, cardID: int):
    card = self.session.query(Card).filter_by(id=cardID).first()
    if card:
      self.session.delete(card)
      self.session.commit()

  def get_recent(self, limit: int = 10) -> List[Card]:
    """Fetch the most recently added cards."""
    return (self.session.query(Card).order_by(Card.updated_at.desc(
    ))  # Assuming there's an added_timestamp attribute in Card
            .limit(limit).all())

  # Very important for translating user input to actionable queries.
  def get_ids_by_name(self, partial_name: str, limit: int = 30) -> List[str]:
    result = self.session.query(Card.id).filter(
        Card.name.ilike(f"%{partial_name}%")).limit(limit).all()
    ids = [row.id for row in result]
    return ids

  def get_ids_by_name_or_type(self,
                              query: str,
                              page: int = 1,
                              per_page: int = 10) -> List[Card]:
    """Search for cards based on a query string with pagination."""
    offset = (page - 1) * per_page
    results = self.session.query(Card).filter(
        or_(Card.name.ilike(f"%{query}%"), Card.type.ilike(
            f"%{query}%"))).offset(offset).limit(per_page).all()
    return results

  def get_ids_by_artist(self, artist: str, limit: int = 10) -> List[str]:
    result = self.session.query(Card.id).filter(
        Card.artist.ilike(f"%{artist}%")).limit(limit).all()
    ids = [row.id for row in result]
    return ids

  def get_card_by_id(self, card_id):
    return self.session.query(Card).filter_by(id=card_id).first()

  def get_cards_by_id(self, card_ids):
    return self.session.query(Card).filter_by(Card.id.in_(card_ids)).all()

  def get_cards_by_name(self, userInput: str, limit: int = 30):
    results = self.session.query(Card).filter(
        Card.name.ilike(f"%{userInput}%")).limit(limit).all()
    return results

  def list_all(self) -> List[Card]:
    """Returns a list of all the cards in the database."""
    return self.session.query(Card).all()
