'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
// import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

interface Metrics {
  total_articles: number;
  total_features: number;
  avg_sentiment: number;
  avg_prediction: number;
  sentiment_dist: {
    positive: number;
    neutral: number;
    negative: number;
  };
}

export function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/metrics`);
      setMetrics(response.data);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !metrics) {
    return (
      <div className="flex justify-center py-12">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-600 border-t-blue-500"></div>
      </div>
    );
  }

  const sentimentData = [
    { name: 'Positive', value: metrics.sentiment_dist.positive, fill: '#10b981' },
    { name: 'Neutral', value: metrics.sentiment_dist.neutral, fill: '#6b7280' },
    { name: 'Negative', value: metrics.sentiment_dist.negative, fill: '#ef4444' }
  ];

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      {/* Stats Cards */}
      <div className="col-span-full grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-4">
          <p className="text-sm text-slate-400">Total Articles</p>
          <p className="mt-2 text-2xl font-bold text-white">{metrics.total_articles}</p>
        </div>
        <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-4">
          <p className="text-sm text-slate-400">Analyzed Features</p>
          <p className="mt-2 text-2xl font-bold text-white">{metrics.total_features}</p>
        </div>
        <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-4">
          <p className="text-sm text-slate-400">Avg Sentiment</p>
          <p className="mt-2 text-2xl font-bold text-blue-400">{metrics.avg_sentiment.toFixed(2)}</p>
        </div>
        <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-4">
          <p className="text-sm text-slate-400">Prediction Avg</p>
          <p className="mt-2 text-2xl font-bold text-cyan-400">{metrics.avg_prediction.toFixed(2)}</p>
        </div>
      </div>

      {/* Sentiment Distribution */}
      <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-6">
        <h2 className="mb-6 text-lg font-semibold text-white">Sentiment Distribution</h2>
        {/* <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={sentimentData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {sentimentData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer> */}
      </div>

      {/* Sentiment Scores */}
      <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-6">
        <h2 className="mb-6 text-lg font-semibold text-white">Key Metrics</h2>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Average Sentiment Score</span>
              <span className="text-white font-semibold">{metrics.avg_sentiment.toFixed(3)}</span>
            </div>
            <div className="mt-2 h-2 rounded-full bg-slate-700">
              <div
                className="h-2 rounded-full bg-gradient-to-r from-red-500 to-green-500"
                style={{ width: `${((metrics.avg_sentiment + 1) / 2) * 100}%` }}
              ></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Model Prediction Confidence</span>
              <span className="text-white font-semibold">{(metrics.avg_prediction * 100).toFixed(1)}%</span>
            </div>
            <div className="mt-2 h-2 rounded-full bg-slate-700">
              <div
                className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500"
                style={{ width: `${metrics.avg_prediction * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
