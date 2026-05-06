from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    load_dotenv()
    # Database setup
    database_url = os.getenv('DATABASE_URL', 'sqlite:///stocknews.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    from app.models import Base
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    app.db_session = scoped_session(sessionmaker(bind=engine))
    
    # Register blueprints
    from app.routes import articles, predict, ingest, news_feed
    app.register_blueprint(articles.bp)
    app.register_blueprint(predict.bp)
    app.register_blueprint(ingest.bp)
    app.register_blueprint(news_feed.bp)
    
    from app.services.scheduler import start_news_scheduler
    start_news_scheduler(app)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        app.db_session.remove()
    
    return app
