from database.random_data_population import RandomDataPopulation
from database.engine import DatabaseEngine

DatabaseEngine.clear_all_tables()
DatabaseEngine.init_db()
session = DatabaseEngine.get_session()
RandomDataPopulation.random_user_card_data(session)
session.close()
