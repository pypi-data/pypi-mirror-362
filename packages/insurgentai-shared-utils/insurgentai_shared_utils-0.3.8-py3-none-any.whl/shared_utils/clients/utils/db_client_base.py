from os import getenv
from abc import ABC, abstractmethod
from typing import Any, ContextManager

class DBClientBase(ABC):
    """Abstract base class for database clients."""
    def __init__(self):
        self.user = getenv("POSTGRES_USER")
        self.password = getenv("POSTGRES_PASSWORD")
        self.host = getenv("POSTGRES_HOST", "localhost")
        self.port = getenv("POSTGRES_PORT", "5432")
        self.dbname = getenv("POSTGRES_DB")

        if not all([self.user, self.password, self.dbname]):
            raise EnvironmentError("Missing required PostgreSQL environment variables")

        # psycopg connection parameters
        self.connection_params = {
            "host": self.host,
            "port": self.port,
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password
        }

    @abstractmethod
    def scoped_session(self) -> ContextManager[Any]:
        """Context manager for scoped database operations with auto commit/rollback/close."""

    @abstractmethod
    def get_persistent_session(self) -> Any:
        """Get a persistent session/connection that caller must manage."""
