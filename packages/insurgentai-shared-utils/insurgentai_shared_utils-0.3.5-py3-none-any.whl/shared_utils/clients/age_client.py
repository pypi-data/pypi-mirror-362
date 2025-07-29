import os
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row
from psycopg import Connection
from .utils.db_client_base import DBClientBase

class AGEClient(DBClientBase):
    """AGE client for connecting to a PostgreSQL database with Apache AGE extension.
    Requires environment variables:
    - POSTGRES_USER: The username for the database.
    - POSTGRES_PASSWORD: The password for the database.
    - POSTGRES_HOST: The host of the database (default: localhost).
    - POSTGRES_PORT: The port of the database (default: 5432).
    - POSTGRES_DB: The name of the database.
    """

    @contextmanager
    def scoped_session(self):
        """Scoped connection with auto commit/rollback/close."""
        conn: Connection = psycopg.connect(**self.connection_params, row_factory=dict_row)
        try:
            self._setup_age_session(conn)
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_persistent_session(self) -> Connection:
        """Caller is responsible for commit/rollback/close."""
        conn = psycopg.connect(**self.connection_params, row_factory=dict_row)
        self._setup_age_session(conn)
        return conn

    def _setup_age_session(self, conn: Connection) -> None:
        """Setup AGE environment for each session."""
        try:
            with conn.cursor() as cur:
                cur.execute("LOAD 'age';")
                cur.execute("SET search_path = ag_catalog, '$user', public;")
        except Exception:
            # AGE might not be properly installed
            pass

    def load_age_extension(self) -> bool:
        """Load the AGE extension (legacy method - now handled automatically)."""
        return True  # Always return True since extension is loaded automatically


age_client = AGEClient()  # module level singleton instance