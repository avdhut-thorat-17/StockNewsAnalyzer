'use client';

import { useState, useEffect } from 'react';
import { ArticleList } from '@/components/article-list';
import { Dashboard } from '@/components/dashboard';
import { PredictionPanel } from '@/components/prediction-panel';

export default function Home() {
  const [activeTab, setActiveTab] = useState('articles');

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700/50 bg-slate-900/50 backdrop-blur">
        <div className="mx-auto max-w-7xl px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">Stock News Analyzer</h1>
              <p className="mt-1 text-sm text-slate-400">AI-powered sentiment analysis for market movements</p>
            </div>
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500">
              <span className="text-lg font-bold text-white">📈</span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b border-slate-700/50 bg-slate-800/30">
        <div className="mx-auto max-w-7xl px-6">
          <div className="flex gap-8">
            <button
              onClick={() => setActiveTab('articles')}
              className={`border-b-2 px-1 py-4 text-sm font-medium transition-colors ${
                activeTab === 'articles'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-slate-400 hover:text-slate-300'
              }`}
            >
              Articles
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`border-b-2 px-1 py-4 text-sm font-medium transition-colors ${
                activeTab === 'dashboard'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-slate-400 hover:text-slate-300'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('predict')}
              className={`border-b-2 px-1 py-4 text-sm font-medium transition-colors ${
                activeTab === 'predict'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-slate-400 hover:text-slate-300'
              }`}
            >
              Predict
            </button>
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="mx-auto max-w-7xl px-6 py-8">
        {activeTab === 'articles' && <ArticleList />}
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'predict' && <PredictionPanel />}
      </div>
    </main>
  );
}
