from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Default SQLite path (can be overridden via .env DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stocktrend.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class PriceCache(Base):
    __tablename__ = "price_cache"
    ticker = Column(String, primary_key=True, index=True)
    data = Column(Text, nullable=False)  # JSON serialized pandas DataFrame
    fetched_at = Column(DateTime, nullable=False)

# Additional tables (watchlist, history) can be added later.

def init_db():
    Base.metadata.create_all(bind=engine)
