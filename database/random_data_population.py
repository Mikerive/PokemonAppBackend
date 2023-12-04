import csv
import requests
import random
from dao.user_dao import UserDAO
from dao.card_dao import CardDAO
from dao.collection_dao import UserCardCollectionDAO
import os


class RandomDataPopulation:

  # User Sample
  @staticmethod
  def populate_user(session):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_path, 'user-sample.csv')
    with open(csv_path, mode='r') as user_sample_file:
      file = csv.DictReader(user_sample_file)

      for row in file:
        #Hash password first

        user_data = {
            'username': row['username'],
            'password': row['password'],
            'email': row['email'],
            'address': row['address'],
            'phoneNumber': row['phoneNumber']
        }
        user_id = UserDAO(session)
        user_id = user_id.create_user(user_data)

  # API Card Sample
  @staticmethod
  def populate_card(session):
    pokemon_api_url = "https://api.pokemontcg.io/v2/cards/"
    api_key = "785c6cce-a764-4997-ba27-6e686092de6b"
    page = 1
    pageSize = 250
    num_of_cards = 500
    pages = num_of_cards / pageSize
    key = {'X-Api-Key': api_key}

    while page <= pages:
      q = {"page": page, "pageSize": pageSize}
      response = requests.get(pokemon_api_url, params=q, headers=key)
      card_data = response.json()

      for card in card_data["data"]:
        card_id = CardDAO(session)
        card_id.create_card(card)
      page += 1

  # Collection Sample (Connect User -> Cards)
  @staticmethod
  def populate_collection(session):
    user_dao = UserDAO(session)
    card_dao = CardDAO(session)
    users = user_dao.list_users()
    cards = card_dao.list_all()
    user_has_cards = 20

    for user in users:
      random_cards = random.choices(cards, k=user_has_cards)
      for card in random_cards:
        user_card = UserCardCollectionDAO(session)
        user_card.add_card_to_collection(user.id, card.id)

  '''
  @staticmethod
  def populate_marketListing(session):
  '''

  # Moved logic to database_reset.py
  @staticmethod
  def random_user_card_data(session):

    RandomDataPopulation.populate_user(session)
    RandomDataPopulation.populate_card(session)
    RandomDataPopulation.populate_collection(session)
