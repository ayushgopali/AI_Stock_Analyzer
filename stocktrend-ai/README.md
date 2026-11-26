# StockTrend AI

A **production‑grade** web app that analyses Indian‑stock (NSE/BSE) tickers, blends historical price data, technical indicators, and finance‑tuned news sentiment to generate a risk‑aware next‑day recommendation (BUY / HOLD / SELL) with stop‑loss / target levels.

---
## Tech stack
- **Backend** – Python 3.11, FastAPI, uvicorn, pandas, numpy, scikit‑learn, yfinance, feedparser, vaderSentiment (FinBERT optional), SQLAlchemy + SQLite.
- **Frontend** – React + Vite + TypeScript, TailwindCSS, Recharts (or lightweight‑charts) for candlesticks.
- **Containerisation** – Docker + Docker‑Compose (single‑command start).
- **Tests** – pytest (backend) & Vitest (frontend).

---
## Quick start (Docker)
```bash
# Clone / copy the repo
cd stocktrend-ai

# Copy env example and adjust if needed
cp .env.example .env

# Build & run everything
docker compose up --build   # backend on 8000, frontend on 3000
```
Open <http://localhost:3000> in your browser.

---
## Local development (without Docker)
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```
### Frontend
```bash
cd frontend
npm install
npm run dev   # Vite dev server on http://localhost:5173
```

---
## Environment variables (`.env.example`)
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite DB URL (SQLAlchemy) | `sqlite:///./stocktrend.db` |
| `YFINANCE_TTL_HOURS` | Cache TTL for price data (hours) | `1` |
| `NEWS_TTL_MINUTES` | Cache TTL for news feeds (minutes) | `10` |
| `FINBERT_TOGGLE` | Set to `true` to use FinBERT instead of VADER | `false` |
| `MODEL_CHOICE` | `logreg`, `rf`, `gb`, `xgb`, `lstm` (default `rf`) | `rf` |
| `MAX_TICKER_AGE_DAYS` | Max age for cached price data before refresh | `1` |
| `LOG_LEVEL` | Logging verbosity (`info`, `debug`, `warning`) | `info` |

---
## API reference
The backend exposes the following endpoints (see `backend/app/routers/` for details):
- `GET /api/analyze?ticker=RELIANCE`
- `GET /api/market`
- `GET /api/watchlist` / `POST /api/watchlist` / `DELETE /api/watchlist`
- `GET /api/history?ticker=`
- `GET /api/scan` – scores all Nifty‑50 tickers and returns top BUY / SELL.
- `GET /api/health`

---
## Known limitations
- Accuracy is modest (≈ 55 % on recent back‑tests); the model is deliberately simple for demo purposes.
- News sentiment uses a lightweight VADER model; FinBERT is optional and may require GPU for good throughput.
- No authentication – the app is intended for personal, educational use only.
- Real‑time price updates are limited by yfinance rate limits; cache TTL helps avoid throttling.

---
## Contributing
Feel free to open PRs to add:
- better feature engineering or additional technical indicators,
- more robust news sources / language models,
- unit/integration tests, or UI polish.

---
## License
MIT – use it however you like, but **not** for regulated financial advice.
