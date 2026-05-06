from app import create_app
from app.models import Base
from sqlalchemy import create_engine
import os

def init_database():
    """Create database tables from models."""
    app = create_app()
    with app.app_context():
        database_url = os.getenv('DATABASE_URL', 'sqlite:///stocknews.db')
        engine = create_engine(database_url)
        print("Creating database tables...")
        Base.metadata.create_all(engine)
        print("Database tables created.")

if __name__ == '__main__':
    init_database()