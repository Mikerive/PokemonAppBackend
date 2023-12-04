from models.collection import UserCardCollection
from models.card import Card
from models.user import User


class UserCardCollectionDAO:

  def __init__(self, session):
    self.session = session

  def add_card_to_collection(self, user_id, card_id, for_sale=False):
    new_entry = UserCardCollection(userID=user_id,
                                   cardID=card_id,
                                   for_sale=for_sale)
    self.session.add(new_entry)
    self.session.commit()

  # Sharding makes it efficient to query the card collection by user_id

  def get_cards_from_collection(self, user_id):
    # Fetch card IDs as a list of tuples
    card_id_tuples = self.session.query(
        UserCardCollection.cardID).filter_by(userID=user_id).all()

    # Extract card IDs from tuples into a flat list
    card_ids = [card_id for (card_id, ) in card_id_tuples]

    # Fetch and return cards using the list of card IDs
    return self.session.query(Card).filter(Card.id.in_(card_ids)).all()

  def update_card_in_collection(self, user_id, qNum, for_sale=None):
    entry = self.session.query(UserCardCollection).filter_by(
        userID=user_id).filter_by(qNum=qNum).first()
    if entry and for_sale is not None:
      entry.for_sale = for_sale
      self.session.commit()

  def delete_card_from_collection(self, user_id, qNum):
    entry = self.session.query(UserCardCollection).filter_by(
        userID=user_id).filter_by(qNum=qNum).first()
    if entry:
      self.session.delete(entry)
      self.session.commit()
