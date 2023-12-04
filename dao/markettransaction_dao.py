from models.transactions import MarketTransactions


class MarketTransactionDAO:

  def __init__(self, session):
    self.session = session

  def create_transaction(self,
                         user_id,
                         cards_data,
                         transaction_price,
                         transaction_status='Pending'):
    transaction = MarketTransactions(
        UserID=user_id,
        cards_data=cards_data,
        transactionPrice=transaction_price,
        transactionStatus=transaction_status,
        # transactionTimestamp will be set automatically to the current timestamp
    )
    self.session.add(transaction)
    self.session.commit()
    return transaction.transactionID

  def get_transaction_by_id(self, transaction_id):
    return self.session.query(MarketTransactions).get(transaction_id)

  def update_transaction(self, transaction_id, updated_data):
    transaction = self.session.query(MarketTransactions).get(transaction_id)
    if not transaction:
      return None
    for key, value in updated_data.items():
      setattr(transaction, key, value)
    self.session.commit()
    return transaction.transactionID

  def delete_transaction(self, transaction_id):
    transaction = self.session.query(MarketTransactions).get(transaction_id)
    if not transaction:
      return False
    self.session.delete(transaction)
    self.session.commit()
    return True

  def list_transactions_by_user(self, user_id):
    return self.session.query(MarketTransactions).filter_by(
        UserID=user_id).all()
