'use client';

import { useState } from 'react';
import axios from 'axios';
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

interface Prediction {
  sentiment: number;
  prediction: number;
  probability: number;
  tickers: Record<string, number>;
  prediction_label: string;
}

export function PredictionPanel() {
  const [text, setText] = useState('');
  const [ticker, setTicker] = useState('');
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/predict`, {
        text,
        ticker: ticker || undefined
      });
      setPrediction(response.data);
    } catch (err) {
      setError('Failed to make prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {/* Input Form */}
      <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-6">
        <h2 className="mb-6 text-lg font-semibold text-white">Test Prediction</h2>
        <form onSubmit={handlePredict} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300">Article Text</label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste article text here..."
              rows={8}
              className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300">Ticker (Optional)</label>
            <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              placeholder="e.g., AAPL"
              className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !text}
            className="w-full rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 px-4 py-2 font-semibold text-white hover:from-blue-600 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {loading ? 'Analyzing...' : 'Predict'}
          </button>
        </form>
        {error && <div className="mt-4 rounded-lg bg-red-500/10 p-3 text-sm text-red-400">{error}</div>}
      </div>

      {/* Results */}
      {prediction && (
        <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-6">
          <h2 className="mb-6 text-lg font-semibold text-white">Prediction Results</h2>
          <div className="space-y-4">
            <div className="rounded-lg bg-slate-900/50 p-4">
              <p className="text-sm text-slate-400">Sentiment Score</p>
              <p className="mt-2 text-2xl font-bold text-blue-400">{prediction.sentiment.toFixed(3)}</p>
              <div className="mt-3 h-2 rounded-full bg-slate-700">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-red-500 to-green-500"
                  style={{ width: `${((prediction.sentiment + 1) / 2) * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="rounded-lg bg-slate-900/50 p-4">
              <p className="text-sm text-slate-400">Prediction</p>
              <div className="mt-2 flex items-center gap-3">
                <div className={`rounded-full px-4 py-2 font-semibold ${
                  prediction.prediction === 1
                    ? 'bg-green-500/20 text-green-400'
                    : 'bg-red-500/20 text-red-400'
                }`}>
                  {prediction.prediction_label}
                </div>
              </div>
              <p className="mt-3 text-sm text-slate-400">Confidence</p>
              <p className="mt-1 text-xl font-bold text-cyan-400">{(prediction.probability * 100).toFixed(1)}%</p>
              <div className="mt-3 h-2 rounded-full bg-slate-700">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500"
                  style={{ width: `${prediction.probability * 100}%` }}
                ></div>
              </div>
            </div>

            {prediction.tickers && Object.keys(prediction.tickers).length > 0 && (
              <div className="rounded-lg bg-slate-900/50 p-4">
                <p className="text-sm text-slate-400">Detected Tickers</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {Object.entries(prediction.tickers).map(([tick, score]) => (
                    <span key={tick} className="inline-block rounded-full bg-blue-500/20 px-3 py-1 text-xs font-medium text-blue-300">
                      ${tick}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
