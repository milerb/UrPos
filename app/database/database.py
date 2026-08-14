from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class Database:
    """Database class."""

    # Define constants here.
    _URL: str = "sqlite:///sample.db"

    # Create the engine.
    _engine = create_engine(url=_URL)

    # Make a session.
    _Session = sessionmaker(bind=_engine)
    _session = _Session()

    @property
    def session(self) -> Session:
        return self._session
