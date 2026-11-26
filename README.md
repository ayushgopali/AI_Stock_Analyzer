# StockTrend AI

A **production‑grade** web application that analyzes Indian‑stock (NSE/BSE) tickers, blends historical price data, technical indicators, and finance‑tuned news sentiment, and returns a risk‑aware next‑day recommendation (BUY / HOLD / SELL) with stop‑loss and target levels.

---

## Table of Contents
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Project Structure](#project-structure)  
- [Installation & Quick Start](#installation--quick-start)  
  - [Option 1 – Docker Compose (one‑command)](#option-1---docker-compose-one‑command)  
  - [Option 2 – Local Development (no Docker)](#option-2---local-development-no-docker)  
- [Running the Application](#running-the-application)  
- [API Reference](#api-reference)  
- [Frontend Overview](#frontend-overview)  
- [Testing](#testing)  
- [Known Limitations & Future Work](#known-limitations--future-work)  
- [License](#license)

---

## Features
- **Historical data**: 5 years of OHLCV fetched from yfinance (`.NS` suffix added automatically).  
- **Technical indicators**: RSI‑14, MACD + histogram, SMA‑20, EMA‑50, Bollinger %B, Stochastic %K, ATR‑14, returns, volume change, volatility.  
- **ML models**: Logistic Regression, Random Forest, Gradient Boosting (XGBoost optional, LSTM optional). Chronological 80/20 split, no shuffling, no look‑ahead leakage.  
- **News sentiment**: RSS feeds + Google News, scored with VADER (FinBERT optional).  
- **Advice engine**: Weighted blend of model probability, stock‑specific sentiment, market sentiment, SMA‑50 trend; crash‑risk flags enforce SELL.  
- **Full API**: `/api/analyze`, `/api/market`, `/api/watchlist`, `/api/history`, `/api/scan`, `/api/health`.  
- **Frontend**: React + Vite + TypeScript, Tailwind CSS (dark/light), Recharts for charts.  
- **Dockerised**: One‑command `docker compose up`.  
- **Persisted storage**: SQLite holds price cache, watchlist, prediction history.

---

## Tech Stack
| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11, FastAPI, uvicorn, pandas, numpy, scikit‑learn, yfinance, feedparser, vaderSentiment (FinBERT optional via 🤗 Transformers), SQLAlchemy + SQLite |
| **Frontend** | React 18, Vite, TypeScript, TailwindCSS, Recharts (or lightweight‑charts) |
| **Containerisation** | Docker, Docker‑Compose |
| **Testing** | pytest (backend), Vitest (frontend) |

---

## Project Structure
