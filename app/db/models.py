from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey,
    Numeric, JSON, TIMESTAMP
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class PlayerProfile(Base):
    __tablename__ = "player_profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    behavior_type = Column(String(20), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    stats = relationship("PlayerStats", back_populates="player")

class BoardProperty(Base):
    __tablename__ = "board_property"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer, unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    rent_price = Column(Numeric(10, 2), nullable=False)
    color_group = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    property_states = relationship("GamePropertyState", back_populates="property")

class GameLog(Base):
    __tablename__ = "game_log"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String(20))
    execution_time = Column(Float)
    winner = Column(String(100))
    details_json = Column(JSON)
    error_message = Column(String)

    result = relationship("GameResult", back_populates="log", uselist=False)

class GameResult(Base):
    __tablename__ = "game_result"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("game_log.id"))
    total_rounds = Column(Integer)
    winner_id = Column(Integer, ForeignKey("player_profile.id"))
    duration = Column(Float)
    finished_reason = Column(String(50))
    status = Column(String(20), default="IN_PROGRESS")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    log = relationship("GameLog", back_populates="result")
    winner = relationship("PlayerProfile")
    rounds = relationship("GameRound", back_populates="game")
    stats = relationship("PlayerStats", back_populates="game")
    properties_state = relationship("GamePropertyState", back_populates="game")

class GameRound(Base):
    __tablename__ = "game_round"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_result.id"))
    round_number = Column(Integer, nullable=False)
    summary = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    game = relationship("GameResult", back_populates="rounds")

class GamePropertyState(Base):
    __tablename__ = "game_property_state"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_result.id"))
    property_id = Column(Integer, ForeignKey("board_property.id"))
    owner_id = Column(Integer, ForeignKey("player_profile.id"), nullable=True)
    purchase_price = Column(Numeric(10, 2))
    current_rent = Column(Numeric(10, 2))
    times_rented = Column(Integer, default=0)
    times_purchased = Column(Integer, default=0)
    status = Column(String(20), default="available")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    game = relationship("GameResult", back_populates="properties_state")
    property = relationship("BoardProperty", back_populates="property_states")

class PlayerStats(Base):
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_result.id"))
    player_id = Column(Integer, ForeignKey("player_profile.id"))
    final_balance = Column(Numeric(10, 2))
    properties_owned = Column(Integer)
    properties_bought = Column(Integer)
    rent_paid_qty = Column(Integer)
    rent_received_qty = Column(Integer)
    rent_paid_total = Column(Numeric(10, 2))
    rent_received_total = Column(Numeric(10, 2))
    total_spent = Column(Numeric(10, 2))
    total_earned = Column(Numeric(10, 2))
    turns_survived = Column(Integer)
    avg_rent_paid = Column(Numeric(10, 2))
    avg_rent_received = Column(Numeric(10, 2))
    net_result = Column(Numeric(10, 2))
    efficiency_ratio = Column(Numeric(10, 2))
    total_transactions = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    player = relationship("PlayerProfile", back_populates="stats")
    game = relationship("GameResult", back_populates="stats")
