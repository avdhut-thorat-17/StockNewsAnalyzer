import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import scipy.sparse

def train_model(articles_data, save_path="models/model_v1.joblib"):
    """
    Train a simple logistic regression model on TF-IDF + sentiment features.
    articles_data: list of dicts with 'text', 'sentiment', 'label' keys
    """
    # Filter out samples without labels
    labeled_data = [a for a in articles_data if a.get('label') is not None]
    
    if len(labeled_data) < 10:
        return None, "Not enough labeled data"
    
    texts = [a['text'] for a in labeled_data]
    sentiments = np.array([[a['sentiment']] for a in labeled_data])
    labels = np.array([1 if a['label'] > 0 else 0 for a in labeled_data])
    
    # Vectorize text
    tfidf = TfidfVectorizer(max_features=5001, ngram_range=(1, 2), min_df=2)
    X_tfidf = tfidf.fit_transform(texts)
    
    # Combine TF-IDF with sentiment
    X_full = scipy.sparse.hstack([X_tfidf, sentiments])
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_full, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Train model
    clf = LogisticRegression(max_iter=1000, class_weight='balanced')
    clf.fit(X_train, y_train)
    
    # Evaluate
    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': np.mean(preds == y_test),
        'roc_auc': roc_auc_score(y_test, probs),
        'report': classification_report(y_test, preds, output_dict=True)
    }
    
    # Save model
    model_artifact = {
        'tfidf': tfidf,
        'clf': clf,
        'metrics': metrics
    }
    joblib.dump(model_artifact, save_path)
    
    return model_artifact, metrics
