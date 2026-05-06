from flask import Blueprint, jsonify, request, current_app
from app.models import Article, ArticleTicker, ArticleFeature
from app.ml.preprocess import compute_features, extract_tickers
from datetime import datetime
import yfinance as yf
import requests
import threading
import xmltodict
from dateutil import parser

bp = Blueprint('news_feed', __name__, url_prefix='/api')

def fetch_news_for_ticker(ticker):
    """Fetch latest news for a specific ticker using yfinance."""
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'DNT': '1', 
            'UPGRADE-INSECURE-REQUESTS': '1'
        })
        
        # Use requests to fetch the RSS feed
        news_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
        response = session.get(news_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the XML content
        data = xmltodict.parse(response.content)
        news = data.get('rss', {}).get('channel', {}).get('item', [])
        
        print(f"Fetched news for {ticker}: {news}")

        articles_added = []
        for article in news:
            # Check if URL already exists
            url = article.get('link')
            if url:
                existing = current_app.db_session.query(Article).filter_by(url=url).first()
                if existing:
                    continue
            
            # Create article
            article_obj = Article(
                source=article.get('source', 'Yahoo Finance'),
                title=article.get('title', 'No Title'),
                content=article.get('description', ''),
                url=url,
                published_at=parser.parse(article.get('pubDate')) if article.get('pubDate') else datetime.utcnow(),
                language='en'
            )
            
            current_app.db_session.add(article_obj)
            current_app.db_session.flush()
            
            # Add ticker relationship
            ticker_obj = ArticleTicker(
                article_id=article_obj.id,
                ticker=ticker,
                score=1.0
            )
            current_app.db_session.add(ticker_obj)
            
            # Compute features
            full_text = f"{article_obj.title} {article_obj.content}"
            features = compute_features(article_obj.title, article_obj.content)
            
            feature_obj = ArticleFeature(
                article_id=article_obj.id,
                ticker=ticker,
                sentiment=features['sentiment'],
                headline_len=features['headline_len'],
                body_len=features['body_len'],
                num_pos=features['num_pos'],
                num_neg=features['num_neg']
            )
            current_app.db_session.add(feature_obj)
            
            articles_added.append({
                'id': article_obj.id,
                'title': article_obj.title,
                'source': article_obj.source
            })
        
        current_app.db_session.commit()
        return articles_added
    
    except Exception as e:
        print(f"Error fetching news for {ticker}: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

@bp.route('/news/fetch/<ticker>', methods=['GET'])
def fetch_ticker_news(ticker):
    """Fetch real-time news for a specific ticker."""
    ticker = ticker.upper()
    articles_added = fetch_news_for_ticker(ticker)
    
    return jsonify({
        'ticker': ticker,
        'articles_added': len(articles_added),
        'articles': articles_added
    }), 200

@bp.route('/news/fetch-multiple', methods=['POST'])
def fetch_multiple_news():
    """Fetch news for multiple tickers."""
    data = request.json
    tickers = data.get('tickers', [])
    
    all_articles = []
    for ticker in tickers:
        articles = fetch_news_for_ticker(ticker.upper())
        all_articles.extend(articles)
    
    return jsonify({
        'total_articles_added': len(all_articles),
        'articles': all_articles
    }), 200

@bp.route('/news/refresh-all', methods=['POST'])
def refresh_all_news():
    """Refresh news for all tracked tickers."""
    # Get unique tickers from database
    tickers_result = current_app.db_session.query(ArticleTicker.ticker).distinct().all()
    tickers = [row[0] for row in tickers_result]
    
    all_articles = []
    for ticker in tickers:
        articles = fetch_news_for_ticker(ticker)
        all_articles.extend(articles)
    
    return jsonify({
        'tickers_processed': len(tickers),
        'total_articles_added': len(all_articles),
        'articles': all_articles
    }), 200
