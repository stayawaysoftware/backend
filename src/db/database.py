"""Database module."""
from pony.orm import Database

db = Database()


def bind_database():
    """Bind the database to the application."""
    if db.provider is None:
        db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
        db.generate_mapping(create_tables=True)
