from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_news_scheduler(app):
    """Start background scheduler for fetching news at regular intervals."""
    from app.routes.news_feed import fetch_news_for_ticker
    
    def scheduled_news_fetch():
        with app.app_context():
            from app.models import ArticleTicker
            
            # Get unique tickers
            tickers_result = app.db_session.query(ArticleTicker.ticker).distinct().all()
            tickers = [row[0] for row in tickers_result]
            
            logger.info(f"Starting scheduled news fetch for {len(tickers)} tickers")
            
            for ticker in tickers:
                try:
                    articles = fetch_news_for_ticker(ticker)
                    logger.info(f"Fetched {len(articles)} articles for {ticker}")
                except Exception as e:
                    logger.error(f"Error fetching news for {ticker}: {str(e)}")
    
    # Schedule news fetch every 1 hour
    scheduler.add_job(
        scheduled_news_fetch,
        trigger=IntervalTrigger(hours=1),
        id='news_fetch_job',
        name='Fetch news every hour',
        replace_existing=True
    )
    
    if not scheduler.running:
        scheduler.start()
        logger.info("News scheduler started")

def stop_news_scheduler():
    """Stop the background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("News scheduler stopped")
