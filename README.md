# 📈 Stock News Analyzer

> **AI-powered sentiment analysis for stock market movements** — Automatically fetches financial news, extracts tickers, performs NLP-based sentiment analysis, and serves predictions through a modern web dashboard.

[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-blue?logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.11-yellow?logo=python)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🗂️ Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Option A — Docker Compose (Recommended)](#option-a--docker-compose-recommended)
  - [Option B — Manual Setup](#option-b--manual-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Stock News Analyzer is a full-stack application that continuously monitors financial news from **Yahoo Finance RSS feeds**, processes articles with **NLP sentiment analysis** (VADER + scikit-learn), and surfaces insights through a clean Next.js dashboard.

It supports:
- Real-time and scheduled news ingestion per ticker (AAPL, TSLA, NVDA, etc.)
- Sentiment scoring and stock-movement prediction
- Interactive dashboard with metrics, article explorer, and a live prediction panel
- PostgreSQL persistence with SQLAlchemy ORM

---

## Features

| Feature | Description |
|---|---|
| 📰 **News Ingestion** | Pulls articles from Yahoo Finance RSS feeds per ticker |
| 🤖 **Sentiment Analysis** | VADER compound scoring + TF-IDF + Logistic Regression classifier |
| 🔮 **Prediction API** | POST any text → get sentiment score + Positive/Negative label |
| ⏰ **Auto-Scheduler** | APScheduler fetches news every hour in the background |
| 📊 **Dashboard** | Metrics overview: avg sentiment, prediction distribution, article count |
| 🗄️ **PostgreSQL / SQLite** | Configurable database (defaults to SQLite for local dev) |
| 🐳 **Docker Compose** | One-command spin-up of frontend, backend, and database |
| 🌗 **Dark UI** | Sleek dark-mode Next.js interface with Tailwind CSS |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Browser (Port 3000)                  │
│          Next.js 14 App — Articles · Dashboard · Predict │
└────────────────────────┬─────────────────────────────────┘
                         │ REST API calls
┌────────────────────────▼─────────────────────────────────┐
│               Flask Backend (Port 5001)                  │
│  ┌───────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │  /api/    │ │  /api/news/  │ │  /api/predict        │ │
│  │  articles │ │  fetch/<t>   │ │  (ML inference)      │ │
│  └───────────┘ └──────┬───────┘ └──────────────────────┘ │
│                       │                                  │
│  ┌────────────────────▼───────────────────┐              │
│  │  ML Layer: VADER Sentiment + Classifier│              │
│  │  Scheduler: APScheduler (hourly fetch) │              │
│  └──────────────────────────────────────  ┘              │
└────────────────────────┬─────────────────────────────────┘
                         │ SQLAlchemy ORM
┌────────────────────────▼─────────────────────────────────┐
│            PostgreSQL 15 (or SQLite for dev)             │
│   articles · article_tickers · article_features          │
│   stock_prices                                           │
└──────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Frontend
- **Next.js 14** (App Router, TypeScript)
- **Tailwind CSS** + Radix UI
- **Recharts** for data visualisation
- **Lucide React** icons

### Backend
- **Flask 3.0** + Flask-CORS
- **SQLAlchemy 2.0** ORM
- **NLTK VADER** — rule-based sentiment analysis
- **scikit-learn** — TF-IDF vectoriser + Logistic Regression
- **yfinance** + **xmltodict** — Yahoo Finance RSS ingestion
- **APScheduler** — background news fetch every hour

### Infrastructure
- **PostgreSQL 15** (production) / **SQLite** (dev fallback)
- **Docker + Docker Compose**
- **python-dotenv** for config

---

## Project Structure

```
StockNewsAnalyzer/
├── app/                        # Next.js app directory
│   ├── layout.tsx
│   ├── page.tsx                # Main page (Articles / Dashboard / Predict tabs)
│   └── globals.css
├── components/                 # React components
│   ├── article-list.tsx
│   ├── dashboard.tsx
│   └── prediction-panel.tsx
├── backend/
│   ├── app/
│   │   ├── __init__.py         # Flask app factory
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── routes/
│   │   │   ├── articles.py     # GET /api/articles, /api/metrics
│   │   │   ├── ingest.py       # POST /api/ingest
│   │   │   ├── news_feed.py    # GET /api/news/fetch/<ticker>
│   │   │   └── predict.py      # POST /api/predict
│   │   ├── ml/
│   │   │   ├── preprocess.py   # VADER sentiment + feature extraction
│   │   │   ├── predict.py      # Model loading + inference
│   │   │   └── trainer.py      # Model training script
│   │   └── services/
│   │       └── scheduler.py    # APScheduler hourly news fetch
│   ├── requirements.txt
│   ├── run.py
│   └── Dockerfile
├── docker-compose.yml
├── frontend.Dockerfile
├── package.json
└── .gitignore
```

---

## Getting Started

### Prerequisites

| Tool | Minimum Version |
|---|---|
| Node.js | 18+ |
| Python | 3.11+ |
| Docker & Docker Compose | Any recent version |
| Git | Any |

> **PostgreSQL is optional for local dev.** If `DATABASE_URL` is not set, the backend defaults to a local SQLite file (`stocknews.db`).

---

### Option A — Docker Compose (Recommended)

This spins up **PostgreSQL + Flask backend + Next.js frontend** in one command.

```bash
# 1. Clone the repo
git clone https://github.com/avdhut-thorat-17/StockNewsAnalyzer.git
cd StockNewsAnalyzer

# 2. Start all services
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:5001 |
| PostgreSQL | localhost:5432 |

To stop:
```bash
docker-compose down
```

To wipe volumes (reset DB):
```bash
docker-compose down -v
```

---

### Option B — Manual Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/avdhut-thorat-17/StockNewsAnalyzer.git
cd StockNewsAnalyzer
```

#### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (first run only)
python -c "import nltk; nltk.download('vader_lexicon')"

# Configure environment
cp .env.example .env            # then edit .env (see below)

# Run the backend
python run.py
```

Backend will be available at **http://localhost:5001**.

#### 3. Frontend Setup

Open a **new terminal** from the project root:

```bash
# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend will be available at **http://localhost:3000**.

---

## Environment Variables

Create `backend/.env` (copy from the template below):

```env
# Database — use SQLite (default) or PostgreSQL
DATABASE_URL=sqlite:///stocknews.db
# DATABASE_URL=postgresql://postgres:password@localhost:5432/stocknews

# Flask environment
FLASK_ENV=development
```

### Environment Variable Reference

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///stocknews.db` | SQLAlchemy database URL |
| `FLASK_ENV` | `development` | Flask environment mode |

> **Note:** The `.env` file is listed in `.gitignore` and will never be committed to version control.

---

## API Reference

All endpoints are prefixed with `/api`.

### Articles

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/articles` | List articles (paginated, filterable by `?ticker=AAPL`) |
| `GET` | `/api/articles/<id>` | Get single article with sentiment features |
| `GET` | `/api/metrics` | Aggregated sentiment & prediction metrics |

#### `GET /api/articles` Query Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | `1` | Page number |
| `per_page` | int | `20` | Results per page |
| `ticker` | string | — | Filter by ticker symbol (e.g. `AAPL`) |

### News Ingestion

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ingest` | Manually ingest a single article |
| `GET` | `/api/news/fetch/<ticker>` | Fetch & store latest news for a ticker |
| `POST` | `/api/news/fetch-multiple` | Fetch news for multiple tickers |
| `POST` | `/api/news/refresh-all` | Refresh news for all tracked tickers |

#### `POST /api/ingest` Body

```json
{
  "title": "Apple beats earnings expectations",
  "source": "Reuters",
  "content": "Apple Inc reported quarterly earnings...",
  "url": "https://example.com/article",
  "published_at": "2024-01-15T10:00:00"
}
```

### Predictions

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/predict` | Run sentiment + ML prediction on arbitrary text |

#### `POST /api/predict` Body

```json
{
  "text": "Tesla stock surges after record deliveries beat analyst expectations",
  "ticker": "TSLA"
}
```

#### Response

```json
{
  "sentiment": 0.7184,
  "prediction": 1,
  "probability": 0.82,
  "prediction_label": "Positive",
  "tickers": { "TSLA": 1 }
}
```

---

## How It Works

### 1. News Ingestion
The scheduler fetches the Yahoo Finance RSS feed for each tracked ticker every **hour**. Articles are deduplicated by URL before being stored.

### 2. Feature Extraction
For each article, the backend computes:
- **VADER compound sentiment** (−1 to +1)
- Headline & body word counts
- Count of bullish / bearish keywords

### 3. ML Prediction
A trained **Logistic Regression** model (with TF-IDF + sentiment features) classifies each article as `Positive` or `Negative` for stock movement. When no trained model is present, the system falls back to pure VADER scoring.

### 4. Dashboard
The Next.js frontend polls the REST API to display:
- Paginated article list with ticker filter
- Sentiment distribution charts
- Live prediction panel for custom text input

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** your changes: `git commit -m "feat: add your feature"`
4. **Push** to the branch: `git push origin feature/your-feature`
5. **Open a Pull Request**

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) format for commit messages.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with ❤️ by <a href="https://github.com/avdhut-thorat-17">avdhut-thorat-17</a></p>
