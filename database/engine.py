import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# Adjusting the DatabaseEngine class based on the suggestions


class DatabaseEngine:
  _instance = None
  _engine = None
  _SessionFactory = None
  _Session = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(DatabaseEngine, cls).__new__(cls)

      # Fetching environment variables with error handling
      try:
        connection_args = {"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}}
        connection_string = os.environ['CONNECTION_STRING']
      except KeyError as e:
        raise Exception(f"Missing environment variable: {e.args[0]}")

      cls._engine = create_engine(connection_string,
                                  connect_args=connection_args)
      cls._SessionFactory = sessionmaker(bind=cls._engine)
      cls._Session = scoped_session(cls._SessionFactory)
    return cls._instance

  @staticmethod
  def get_engine():
    return DatabaseEngine()._engine

  @staticmethod
  def get_session():
    """
        Fetch a new database session.
        """
    return DatabaseEngine()._Session()

  @staticmethod
  def close_session(session):
    """
        Close the provided session.
        """
    session.close()

  @staticmethod
  def init_db():
    """
        Initialize the database, create tables based on models.
        """
    from models.base import Base  # Importing Base object from your models
    Base.metadata.create_all(bind=DatabaseEngine.get_engine())

  @staticmethod
  def clear_all_tables():
    """
        Drop all tables from the database.
        """
    from models.base import Base  # Importing Base object from your models
    Base.metadata.drop_all(bind=DatabaseEngine.get_engine())
