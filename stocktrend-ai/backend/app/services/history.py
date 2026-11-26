from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    id = Column(String, primary_key=True)
    ticker = Column(String, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    prob_up = Column(Float)
    recommendation = Column(String)
    actual_close = Column(Float, nullable=True)  # filled later when actual price known
