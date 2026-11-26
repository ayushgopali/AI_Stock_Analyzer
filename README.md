StockTrend AI

A production‑grade web application that analyzes Indian‑stock (NSE/BSE) tickers, blends historical price data, technical indicators, and finance‑tuned news sentiment, and returns a risk‑aware next‑day recommendation (BUY / HOLD / SELL) with stop‑loss and target levels.

Table of Contents
Features
Tech Stack
Project Structure
Installation & Quick Start
Option 1 – Docker Compose (one‑command)
Option 2 – Local Development (no Docker)
Running the Application
API Reference
Frontend Overview
Testing
Known Limitations & Future Work
License
Features
Historical data: 5 years of OHLCV fetched from yfinance (.NS suffix added automatically).
Technical indicators: RSI‑14, MACD + histogram, SMA‑20, EMA‑50, Bollinger %B, Stochastic %K, ATR‑14, 1‑d/5‑d returns, volume change, 10‑day volatility.
ML models: Logistic Regression, Random Forest, Gradient Boosting (XGBoost optional, LSTM optional). Chronological 80/20 split, no shuffling, no look‑ahead leakage.
News sentiment: RSS feeds from Economic Times, Livemint, Moneycontrol, plus Google News search. Sentiment scored with VADER (FinBERT optional).
Advice engine: Weighted combination of model probability (45 %), stock‑specific sentiment (25 %), market sentiment (10 %), SMA‑50 trend (20 %). Crash‑risk flags (volatility spikes, price‑below‑SMA‑50 + negative MACD, negative market sentiment, >20 % draw‑down, RSI > 75) force SELL. Provides stop‑loss (2 × ATR) and target (3 × ATR).
Full API: /api/analyze, /api/market, /api/watchlist (CRUD), /api/history, /api/scan, /api/health.
Frontend: React + Vite + TypeScript, Tailwind CSS (dark/light themes), Recharts for candlesticks and other charts.
Dockerised: One‑command docker compose up builds and runs both backend and frontend.
Persisted storage: SQLite database stores price cache, watchlist, and prediction history.
Tech Stack
Layer	Technology
Backend	Python 3.11, FastAPI, uvicorn, pandas, numpy, scikit‑learn, yfinance, feedparser, vaderSentiment (FinBERT optional via 🤗 Transformers), SQLAlchemy + SQLite
Frontend	React 18, Vite, TypeScript, TailwindCSS, Recharts (or lightweight‑charts)
Containerisation	Docker, Docker‑Compose
Testing	pytest (backend), Vitest (frontend)
Project Structure
stocktrend-ai/
├─ backend/
│  ├─ app/
│  │  ├─ main.py                # FastAPI entry point
│  │  ├─ routers/               # API routers (analyze, market, watchlist, …)
│  │  ├─ schemas.py             # Pydantic response models
│  │  ├─ db.py                  # SQLite + SQLAlchemy setup
│  │  └─ services/              # data, features, models, news, sentiment, advice, watchlist, history
│  ├─ requirements.txt
│  └─ Dockerfile.backend
├─ frontend/
│  ├─ src/
│  │  ├─ main.tsx               # React bootstrap + BrowserRouter
│  │  ├─ App.tsx                # Nav bar + route definitions
│  │  ├─ api.ts                 # Axios wrapper (proxy → backend)
│  │  ├─ components/            # LoadingSpinner, ErrorBanner, RecommendationCard …
│  │  └─ pages/                 # Predict, Chart, Models, Features, News, Watchlist, History
│  ├─ index.html
│  ├─ package.json
│  ├─ vite.config.ts
│  ├─ tailwind.config.js
│  └─ tsconfig.json
├─ docker-compose.yml
├─ .env.example                # copy to .env and edit if needed
└─ README.md
Installation & Quick Start
Prerequisites
Docker Desktop (if you want the one‑command approach) or
Python 3.11 (official installer from python.org) and Node 20+ (includes npm).
Git (optional, for cloning).
Option 1 – Docker Compose (recommended for a hassle‑free start)
bash
# Clone the repo (if you haven’t already)
git clone https://github.com/ayushgopali/AI_Stock_Analyzer.git
cd AI_Stock_Analyzer
# Copy the example .env and edit if needed (defaults work for a local run)
cp .env.example .env
# Build and start everything
docker compose up --build
Backend API: http://localhost:8000
Front‑end UI: http://localhost:3000
SQLite data lives in a Docker volume (sqlite_data).
Option 2 – Local Development (no Docker)
Backend
bash
cd backend
python -m venv .venv            # create virtual env (Python 3.11 must be on PATH)
.\.venv\Scripts\activate.bat    # Windows cmd – use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
Frontend
bash
cd ../frontend
npm install                     # only the first time
npm run dev                     # Vite dev server → http://localhost:3000

The Vite config proxies any /api/* request to http://localhost:8000, so CORS is handled automatically.

Running the Application
Open a browser to http://localhost:3000.
Use the Predict page: type a ticker (e.g., RELIANCE, TCS, INFY, HDFCBANK) and click Analyze.
The backend will:
Train (or load) the best ML model for the ticker (first run may take a few seconds).
Pull the latest news, compute sentiment, and run the advice engine.
Return a JSON payload that the UI displays as a recommendation card (BUY / HOLD / SELL, confidence, stop‑loss, target, risk flags, reasons).
Explore other pages: Chart, Models, Features, News, Watchlist, History.
API Reference
Endpoint	Method	Description
/api/analyze?ticker=	GET	Returns a recommendation for the supplied ticker.
/api/market	GET	Market‑wide news and aggregated sentiment.
/api/watchlist	GET/POST/DELETE	CRUD operations for the personal watchlist.
/api/history?ticker=	GET	Past predictions vs. actual close prices for the ticker.
/api/scan	GET	Scores all Nifty‑50 tickers; returns top BUY and top SELL candidates.
/api/health	GET	Simple health check ({"status":"ok"}).

All responses are typed Pydantic models and CORS‑enabled for the frontend.

Frontend Overview
React + Vite with Tailwind CSS (dark mode via the class strategy).
Routing handled by react-router-dom – pages: Predict, Chart, Models, Features, News, Watchlist, History.
Key components:
RecommendationCard – shows ticker, recommendation badge, confidence bar, stop‑loss/target, risk level, and a list of reasons.
LoadingSpinner / ErrorBanner – graceful UI feedback.
Chart components (candlestick, SMA, EMA, Bollinger) built with Recharts (you can swap to lightweight‑charts if preferred).
API client (src/api.ts) uses Axios; Vite’s dev server proxies /api/* to the backend automatically.
Testing
Backend (pytest)
bash
cd backend
.\.venv\Scripts\activate.bat
pytest app/tests          # create test files under backend/app/tests as needed
Frontend (Vitest)
bash
cd frontend
npm run test            # runs Vitest – add tests under src/__tests__

Both test suites are wired into the Dockerfile (optional) and can be run in CI.

Known Limitations & Future Work
Model accuracy is modest (≈ 55‑60 % on recent back‑tests) – the pipeline is deliberately simple for demonstration purposes.
FinBERT sentiment model is optional; enabling it requires downloading a ~300 MB transformer model on first use.
No authentication – the app is intended for personal/educational use only.
SQLite works for a single‑user local setup; a production deployment would replace it with a proper RDBMS.
Real‑time price updates are limited by yfinance rate limits; a cache TTL of 1 hour mitigates throttling.
Future improvements: add XGBoost/LSTM training, integrate a scheduler for nightly model retraining, enable user authentication, expand the UI with more visual analytics, add CI/CD pipelines.
License

MIT – Feel free to use, modify, and share. Do not treat this as SEBI‑registered investment advice; the disclaimer in the UI reminds users it is for educational purposes only
