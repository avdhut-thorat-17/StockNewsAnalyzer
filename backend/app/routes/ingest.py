from flask import Blueprint, request, jsonify, current_app
from app.models import Article, ArticleTicker, ArticleFeature
from app.ml.preprocess import compute_features, extract_tickers
from datetime import datetime

bp = Blueprint('ingest', __name__, url_prefix='/api')

@bp.route('/ingest', methods=['POST'])
def ingest_article():
    """Ingest a single news article."""
    data = request.json
    
    required = ['title', 'source']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields: title, source'}), 400
    
    # Check if URL already exists
    if data.get('url'):
        existing = current_app.db_session.query(Article).filter_by(url=data['url']).first()
        if existing:
            return jsonify({'error': 'Article already exists', 'id': existing.id}), 409
    
    # Create article
    article = Article(
        source=data['source'],
        title=data['title'],
        content=data.get('content'),
        url=data.get('url'),
        published_at=datetime.fromisoformat(data['published_at']) if data.get('published_at') else datetime.utcnow(),
        language=data.get('language', 'en')
    )
    
    current_app.db_session.add(article)
    current_app.db_session.flush()
    
    # Extract tickers
    full_text = f"{article.title} {article.content or ''}"
    tickers_found = extract_tickers(full_text)
    
    for ticker, score in tickers_found.items():
        ticker_obj = ArticleTicker(article_id=article.id, ticker=ticker, score=score/len(tickers_found) if tickers_found else 1.0)
        current_app.db_session.add(ticker_obj)
    
    # Compute features for each ticker
    features = compute_features(article.title, article.content)
    
    for ticker in tickers_found.keys():
        feature_obj = ArticleFeature(
            article_id=article.id,
            ticker=ticker,
            sentiment=features['sentiment'],
            headline_len=features['headline_len'],
            body_len=features['body_len'],
            num_pos=features['num_pos'],
            num_neg=features['num_neg']
        )
        current_app.db_session.add(feature_obj)
    
    current_app.db_session.commit()
    
    return jsonify({
        'id': article.id,
        'message': 'Article ingested successfully',
        'tickers_found': list(tickers_found.keys())
    }), 201
