import os
from contextlib import contextmanager
from sqlmodel import Session, create_engine
from .utils.db_client_base import DBClientBase

class DBClient(DBClientBase):
    """Database client for connecting to a Postgres database.
    Requires environment variables:
    - POSTGRES_USER: The username for the database.
    - POSTGRES_PASSWORD: The password for the database.
    - POSTGRES_HOST: The host of the database (default: localhost).
    - POSTGRES_PORT: The port of the database (default: 5432).
    - POSTGRES_DB: The name of the database.
    """
    def __init__(self):
        super().__init__()
        self.database_url = f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        self.engine = create_engine(self.database_url, echo=False)

    @contextmanager
    def scoped_session(self):
        """Scoped session with auto commit/rollback/close."""
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_persistent_session(self) -> Session:
        """Caller is responsible for commit/rollback/close."""
        return Session(self.engine)


db_client = DBClient()  # module level singleton instance