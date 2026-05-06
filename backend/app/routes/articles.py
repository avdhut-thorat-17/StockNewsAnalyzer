from flask import Blueprint, request, jsonify, current_app
from app.models import Article, ArticleFeature, ArticleTicker
from sqlalchemy import desc, func
from datetime import datetime

bp = Blueprint('articles', __name__, url_prefix='/api')

@bp.route('/articles', methods=['GET'])
def list_articles():
    """List articles with pagination and ticker filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    ticker = request.args.get('ticker')
    
    query = current_app.db_session.query(Article)
    
    if ticker:
        query = query.join(ArticleTicker).filter(ArticleTicker.ticker == ticker.upper()).distinct()
    
    total = query.count()
    articles = query.order_by(desc(Article.published_at)).offset((page-1)*per_page).limit(per_page).all()
    
    return jsonify({
        'articles': [{
            'id': a.id,
            'source': a.source,
            'title': a.title,
            'url': a.url,
            'published_at': a.published_at.isoformat() if a.published_at else None,
            'tickers': [t.ticker for t in a.tickers]
        } for a in articles],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    })

@bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get single article with features and predictions."""
    article = current_app.db_session.query(Article).filter_by(id=article_id).first()
    
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    features = current_app.db_session.query(ArticleFeature).filter_by(article_id=article_id).all()
    
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'source': article.source,
        'url': article.url,
        'published_at': article.published_at.isoformat() if article.published_at else None,
        'tickers': [t.ticker for t in article.tickers],
        'features': [{
            'ticker': f.ticker,
            'sentiment': f.sentiment,
            'prediction': f.prob,
            'label': 'Positive' if f.prob > 0.5 else 'Negative'
        } for f in features]
    })

@bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Get model evaluation metrics."""
    # Aggregate sentiment and prediction stats
    features = current_app.db_session.query(ArticleFeature).all()
    
    if not features:
        return jsonify({'metrics': {}, 'message': 'No data available'})
    
    sentiments = [f.sentiment for f in features if f.sentiment is not None]
    predictions = [f.prob for f in features if f.prob is not None]
    
    return jsonify({
        'total_articles': current_app.db_session.query(Article).count(),
        'total_features': len(features),
        'avg_sentiment': sum(sentiments) / len(sentiments) if sentiments else 0,
        'avg_prediction': sum(predictions) / len(predictions) if predictions else 0,
        'sentiment_dist': {
            'positive': sum(1 for s in sentiments if s > 0.1),
            'neutral': sum(1 for s in sentiments if -0.1 <= s <= 0.1),
            'negative': sum(1 for s in sentiments if s < -0.1)
        }
    })
