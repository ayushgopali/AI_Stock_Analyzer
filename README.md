<h1 align="center">📈 STOCKTREND AI</h1>

<h2 align="center">AI-Powered Stock Analyzer for the Indian Market (NSE / BSE)</h2>

<p align="center"><b>Technical indicators + live news sentiment → risk-aware next-day BUY / HOLD / SELL advice</b></p>

<p align="center">
Python 3.11 · FastAPI · React 18 · TypeScript · scikit-learn · Docker
</p>

> ⚠️ **Disclaimer:** This is an educational project and **not SEBI-registered investment advice**. Short-term stock predictions are uncertain. Never invest money you cannot afford to lose.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Limitations](#-limitations)
- [Roadmap](#-roadmap)
- [Team](#-team)
- [License](#-license)

---

## 🔍 Overview

StockTrend AI takes an NSE ticker (e.g. `RELIANCE`, `TCS`), trains machine-learning models on five years of price history and technical indicators, reads the latest Indian market and company news, and returns a recommendation with **stop-loss**, **target**, and **crash-risk warnings**.

It frames the problem as a simple, reproducible **binary classification**: will the stock close **UP** or **DOWN** tomorrow?

## ✨ Features

| Area | What you get |
|---|---|
| **Market data** | 5 years of OHLCV from `yfinance` (`.NS` suffix added automatically) |
| **Technical indicators** | RSI-14, MACD + histogram, SMA-20, EMA-50, Bollinger %B, Stochastic %K, ATR-14, 1d/5d returns, volume change, 10-day volatility |
| **ML models** | Logistic Regression, Random Forest, Gradient Boosting (XGBoost & LSTM optional) |
| **Honest evaluation** | Chronological 80/20 split, no shuffling, no look-ahead leakage; accuracy, precision, recall, F1, confusion matrix |
| **News sentiment** | Live RSS from Economic Times, Livemint, Moneycontrol and Google News, scored with VADER (FinBERT optional) |
| **Advice engine** | Weighted BUY / HOLD / SELL with crash-risk detection, ATR-based stop-loss and target |
| **Explainability** | Feature-importance charts and per-prediction reasons |
| **Watchlist & scanner** | Save tickers; scan the Nifty 50 for top BUY / SELL candidates |
| **Prediction history** | Compare past predictions with actual outcomes |
| **UI** | React dashboard with dark/light themes, candlestick charts, responsive layout |
| **Deployment** | One-command Docker Compose setup, SQLite persistence |

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn, pandas, NumPy, scikit-learn, yfinance, feedparser, vaderSentiment, SQLAlchemy + SQLite |
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS, Recharts, Axios, React Router |
| **DevOps** | Docker, Docker Compose |
| **Testing** | pytest (backend), Vitest (frontend) |

## 🧠 How It Works

```
 Data Acquisition ──► Feature Engineering ──► Model Training ──► Prediction
   (yfinance)          (11 indicators)        (3+ ML models)     P(UP tomorrow)
                                                                      │
 News Collection ───► Sentiment Scoring ───────────────────────────► │
 (RSS feeds)          (VADER / FinBERT)                               ▼
                                                              Advice Engine
                                                     BUY / HOLD / SELL + risk flags
```

### Advice engine weights

| Signal | Weight |
|---|---|
| Model probability of UP | 45% |
| Stock-specific news sentiment | 25% |
| SMA-50 trend | 20% |
| Overall market sentiment | 10% |

### Crash-risk flags

Any **High** risk rating (3 or more flags) forces a **SELL**:

- Volatility spike versus the 60-day norm
- Price below SMA-50 with negative MACD
- Negative overall market sentiment
- More than 20% drawdown from the 52-week high
- RSI above 75 (overbought)

**Stop-loss** = price − 2 × ATR · **Target** = price + 3 × ATR

## 📁 Project Structure

```
AI_Stock_Analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── routers/             # analyze, market, watchlist, history, scan
│   │   ├── services/            # data, features, models, news, sentiment, advice
│   │   ├── schemas.py           # Pydantic response models
│   │   ├── db.py                # SQLAlchemy + SQLite setup
│   │   └── tests/
│   ├── requirements.txt
│   └── Dockerfile.backend
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api.ts               # Axios client
│   │   ├── components/          # RecommendationCard, LoadingSpinner, ErrorBanner...
│   │   └── pages/               # Predict, Chart, Models, Features, News, Watchlist, History
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- **Docker Desktop**, *or*
- **Python 3.11+** and **Node.js 20+**
- Git

### Option 1: Docker Compose (recommended)

```bash
git clone https://github.com/ayushgopali/AI_Stock_Analyzer.git
cd AI_Stock_Analyzer

cp .env.example .env        # defaults work for a local run
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |

SQLite data persists in the `sqlite_data` Docker volume.

### Option 2: Local development

**Backend**

```bash
cd backend
python -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows (cmd)
.venv\Scripts\activate.bat

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend** (in a second terminal)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. The Vite dev server proxies `/api/*` to `http://localhost:8000`, so no CORS setup is needed.

### Using the app

1. Open the **Predict** page and enter a ticker (e.g. `RELIANCE`, `TCS`, `INFY`, `HDFCBANK`).
2. Click **Analyze**. The first run trains the models and may take a few seconds.
3. Review the recommendation, confidence, stop-loss, target and risk flags.
4. Explore **Chart**, **Models**, **Features**, **News**, **Watchlist** and **History**.

## 🔌 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/analyze?ticker=` | GET | Full analysis and recommendation for a ticker |
| `/api/market` | GET | Market-wide news and aggregated sentiment |
| `/api/watchlist` | GET / POST / DELETE | Manage your personal watchlist |
| `/api/history?ticker=` | GET | Past predictions versus actual outcomes |
| `/api/scan` | GET | Scores all Nifty 50 stocks; returns top BUY and SELL ideas |
| `/api/health` | GET | Health check: `{"status": "ok"}` |

**Example**

```bash
curl "http://localhost:8000/api/analyze?ticker=RELIANCE"
```

```json
{
  "ticker": "RELIANCE.NS",
  "prediction": { "direction": "UP", "confidence": 58.4 },
  "advice": {
    "action": "BUY",
    "risk": "Low",
    "stop_loss": 2850.10,
    "target": 3020.55
  }
}
```

Interactive docs are available at `/docs` when the backend is running.

## 🧪 Testing

```bash
# Backend
cd backend
pytest app/tests

# Frontend
cd frontend
npm run test
```

## ⚠️ Limitations

- Model accuracy is modest (about 55–60% on recent back-tests). Treat output as decision support, not a guarantee.
- FinBERT is optional and downloads a ~300 MB model on first use.
- No authentication; intended for personal and educational use.
- SQLite suits a single-user setup; production would need a proper RDBMS.
- Live prices depend on `yfinance` rate limits (mitigated by a 1-hour cache).

## 🗺️ Roadmap

- [ ] XGBoost and LSTM/GRU models
- [ ] Nightly model retraining scheduler
- [ ] Fundamental and earnings-based signals
- [ ] Backtesting and portfolio / risk analysis
- [ ] Explainable AI (SHAP)
- [ ] User authentication
- [ ] CI/CD pipeline

## 👥 Team

CSE AI Research Project, 2026

- **Ayush Harshavardhana Gopali**
- **Aditya Joseph**
- **Bharath S Adiga**

## 📄 License

Released under the [MIT License](LICENSE). Use it freely, but remember this is **not financial advice**.
