import joblib
import scipy.sparse
from app.ml.preprocess import compute_sentiment, extract_tickers

def load_model(model_path="models/model_v1.joblib"):
    """Load trained model artifact."""
    try:
        return joblib.load(model_path)
    except:
        return None

def predict_sentiment(text, ticker=None):
    """Predict using trained model."""
    model_artifact = load_model()
    
    if model_artifact is None:
        return {
            'sentiment': compute_sentiment(text),
            'prediction': None,
            'probability': None,
            'error': 'Model not trained yet'
        }
    
    tfidf = model_artifact['tfidf']
    clf = model_artifact['clf']
    
    sentiment = compute_sentiment(text)
    X_tfidf = tfidf.transform([text])
    X_full = scipy.sparse.hstack([X_tfidf, [[sentiment]]])
    
    pred = clf.predict(X_full)[0]
    prob = clf.predict_proba(X_full)[0, 1]
    
    tickers = extract_tickers(text) if ticker is None else {ticker: 1}
    
    return {
        'sentiment': float(sentiment),
        'prediction': int(pred),
        'probability': float(prob),
        'tickers': tickers,
        'prediction_label': 'Positive' if pred == 1 else 'Negative'
    }
