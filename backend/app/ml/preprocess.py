import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def compute_sentiment(text):
    """Compute VADER sentiment score (compound: -1 to 1)."""
    if not text:
        return 0.0
    return sia.polarity_scores(text)['compound']

def extract_tickers(text, ticker_list=None):
    """Extract potential tickers from text using regex patterns."""
    if ticker_list is None:
        ticker_list = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA']
    
    tickers_found = {}
    text_lower = text.lower()
    
    # Look for $TICKER pattern
    matches = re.findall(r'\$([A-Z]{1,5})', text)
    for match in matches:
        tickers_found[match] = tickers_found.get(match, 0) + 1
    
    # Look for known company names/tickers
    for ticker in ticker_list:
        if ticker.lower() in text_lower:
            tickers_found[ticker] = tickers_found.get(ticker, 0) + 1
    
    return tickers_found

def compute_features(title, content):
    """Extract basic text features."""
    full_text = f"{title} {content}" if content else title
    sentiment = compute_sentiment(full_text)
    
    features = {
        'sentiment': sentiment,
        'headline_len': len(title.split()),
        'body_len': len(content.split()) if content else 0,
        'num_pos': len(re.findall(r'\b(positive|bullish|up|gain|rise|surge|rally)\b', content.lower() if content else '')),
        'num_neg': len(re.findall(r'\b(negative|bearish|down|loss|fall|drop|plunge)\b', content.lower() if content else ''))
    }
    return features
