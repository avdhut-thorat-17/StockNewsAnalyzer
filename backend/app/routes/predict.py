from flask import Blueprint, request, jsonify
from app.ml.predict import predict_sentiment

bp = Blueprint('predict', __name__, url_prefix='/api')

@bp.route('/predict', methods=['POST'])
def predict():
    """Predict sentiment and stock movement for given text."""
    data = request.json
    text = data.get('text', '')
    ticker = data.get('ticker')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    result = predict_sentiment(text, ticker)
    return jsonify(result)
