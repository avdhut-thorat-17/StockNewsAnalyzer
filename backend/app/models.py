from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Numeric, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    source = Column(String(100))
    title = Column(Text, nullable=False)
    content = Column(Text)
    url = Column(Text, unique=True)
    published_at = Column(DateTime)
    saved_at = Column(DateTime, default=datetime.utcnow)
    language = Column(String(10), default='en')
    
    tickers = relationship("ArticleTicker", back_populates="article", cascade="all, delete-orphan")
    features = relationship("ArticleFeature", back_populates="article", cascade="all, delete-orphan")

class ArticleTicker(Base):
    __tablename__ = "article_tickers"
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    ticker = Column(String(20), nullable=False)
    score = Column(Float, default=1.0)
    
    article = relationship("Article", back_populates="tickers")

class StockPrice(Base):
    __tablename__ = "stock_prices"
    id = Column(Integer, primary_key=True)
    ticker = Column(String(20), nullable=False, index=True)
    price_date = Column(DateTime, nullable=False, index=True)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    volume = Column(BigInteger)

class ArticleFeature(Base):
    __tablename__ = "article_features"
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    ticker = Column(String(20), nullable=False)
    sentiment = Column(Float)
    headline_len = Column(Integer)
    body_len = Column(Integer)
    num_pos = Column(Integer)
    num_neg = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    label = Column(Integer, nullable=True)
    prob = Column(Float, nullable=True)
    model_version = Column(String(50), default="v1")
    
    article = relationship("Article", back_populates="features")
