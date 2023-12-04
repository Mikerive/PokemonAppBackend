from dao.markettransaction_dao import MarketTransactionDAO
from typing import List, Dict
from database.engine import DatabaseEngine
import json


class MarketTransactionService:

  @staticmethod
  # Function to create a transaction after purchase confirmation
  def create_transaction(user_id: int, listings: List[Dict]):
    # Aggregate listing data
    transaction_data = {"listings": listings}
    serialized_transaction_data = json.dumps(transaction_data)

    session = DatabaseEngine().get_session()

    # Create a new MarketTransactions instance
    new_transaction = MarketTransactionDAO(session).create_transaction(
        user_id=user_id,
        cards_data=serialized_transaction_data,
        transaction_price=sum(listing['price'] for listing in listings),
        transaction_status='Pending')  # Assuming initial status is 'Pending'

    # Add the transaction to the session and commit
    session.add(new_transaction)
    session.commit()
    session.close()
    return new_transaction

  @staticmethod
  def delete_transaction(transaction_id: int):
    session = DatabaseEngine().get_session()
    success = MarketTransactionDAO(session).delete_transaction(transaction_id)
    session.close()
    return success