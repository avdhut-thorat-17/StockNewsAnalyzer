'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

interface Article {
  id: number;
  title: string;
  source: string;
  url: string;
  published_at: string;
  tickers: string[];
}

export function ArticleList() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [ticker, setTicker] = useState('');
  const [refreshing, setRefreshing] = useState(false);
  const [lastRefresh, setLastRefresh] = useState<string>('');

  useEffect(() => {
    fetchArticles();
  }, [page, ticker]);

  const fetchArticles = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:5001/api/articles', {
        params: { page, per_page: 10, ticker: ticker || undefined }
      });
      setArticles(response.data.articles);
    } catch (error) {
      console.error('Failed to fetch articles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshNews = async () => {
    setRefreshing(true);
    try {
      await axios.post('http://localhost:5001/api/news/refresh-all');
      setLastRefresh(new Date().toLocaleTimeString());
      // Refresh articles list
      await fetchArticles();
    } catch (error) {
      console.error('Failed to refresh news:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleFetchTickerNews = async (tickerSymbol: string) => {
    setRefreshing(true);
    try {
      await axios.get(`http://localhost:5001/api/news/fetch/${tickerSymbol}`);
      setLastRefresh(new Date().toLocaleTimeString());
      // Refresh articles list
      await fetchArticles();
    } catch (error) {
      console.error('Failed to fetch news for ticker:', error);
    } finally {
      setRefreshing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Filter and Controls */}
      <div className="flex gap-4 flex-wrap">
        <input
          type="text"
          placeholder="Filter by ticker (e.g., AAPL)"
          value={ticker}
          onChange={(e) => {
            setTicker(e.target.value.toUpperCase());
            setPage(1);
          }}
          className="flex-1 min-w-48 rounded-lg border border-slate-600 bg-slate-800 px-4 py-2 text-white placeholder-slate-400 focus:border-blue-500 focus:outline-none"
        />
        
        <button
          onClick={handleRefreshNews}
          disabled={refreshing}
          className="rounded-lg bg-blue-600 hover:bg-blue-700 disabled:bg-blue-600 disabled:opacity-50 px-6 py-2 text-white font-medium transition-colors flex items-center gap-2"
        >
          {refreshing ? (
            <>
              <span className="animate-spin">⟳</span>
              Refreshing...
            </>
          ) : (
            <>
              <span>⟳</span>
              Refresh News
            </>
          )}
        </button>

        {lastRefresh && (
          <div className="flex items-center text-sm text-slate-400">
            Last refresh: {lastRefresh}
          </div>
        )}
      </div>

      {/* Articles Grid */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-600 border-t-blue-500"></div>
        </div>
      ) : articles.length === 0 ? (
        <div className="rounded-lg border border-slate-700 bg-slate-800/50 py-12 text-center text-slate-400">
          No articles found. Start by ingesting some news articles.
        </div>
      ) : (
        <div className="space-y-4">
          {articles.map((article) => (
            <div key={article.id} className="rounded-lg border border-slate-700 bg-slate-800/50 p-4 hover:border-slate-600 hover:bg-slate-800/70 transition-colors">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <a href={article.url} target="_blank" rel="noopener noreferrer" className="group">
                    <h3 className="text-lg font-semibold text-white group-hover:text-blue-400 transition-colors line-clamp-2">
                      {article.title}
                    </h3>
                  </a>
                  <p className="mt-2 text-sm text-slate-400">{article.source}</p>
                  {article.tickers.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {article.tickers.map((tick) => (
                        <button
                          key={tick}
                          onClick={() => handleFetchTickerNews(tick)}
                          disabled={refreshing}
                          className="inline-block rounded-full bg-blue-500/20 hover:bg-blue-500/40 disabled:opacity-50 px-3 py-1 text-xs font-medium text-blue-300 transition-colors cursor-pointer"
                          title={`Fetch latest news for ${tick}`}
                        >
                          ${tick}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                <div className="text-right text-sm text-slate-500">
                  {article.published_at && new Date(article.published_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      <div className="flex justify-center gap-4">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
          className="rounded-lg border border-slate-600 px-4 py-2 text-sm font-medium text-slate-300 hover:border-slate-500 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <span className="flex items-center px-4 text-sm text-slate-400">Page {page}</span>
        <button
          onClick={() => setPage(p => p + 1)}
          className="rounded-lg border border-slate-600 px-4 py-2 text-sm font-medium text-slate-300 hover:border-slate-500 hover:text-white"
        >
          Next
        </button>
      </div>
    </div>
  );
}
