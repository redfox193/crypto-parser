from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    statistics = relationship("Statistic", back_populates="symbol")


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    symbol_name = Column(String, ForeignKey("symbols.name"), nullable=False)
    time = Column(DateTime, nullable=False)
    buy = Column(String, nullable=False)
    sell = Column(String, nullable=False)
    change_rate = Column(String, nullable=False)
    change_price = Column(String, nullable=False)
    high = Column(String, nullable=False)
    low = Column(String, nullable=False)
    vol = Column(String, nullable=False)
    vol_value = Column(String, nullable=False)
    last = Column(String, nullable=False)
    average_price = Column(String, nullable=False)

    symbol = relationship("Symbol", back_populates="statistics")
