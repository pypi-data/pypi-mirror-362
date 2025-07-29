"""
Tiny, self-contained persistence layer for SyntaxMatrix.
Uses plain SQLAlchemy + SQLite; no Flask wiring needed.
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1️⃣  Location = uploads/smx.db
DB_PATH = os.path.join(os.getcwd(), "data", "llms.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

# 2️⃣  Workspace table
class Workspace(Base):
    __tablename__ = "workspace"
    id           = Column(Integer, primary_key=True)
    name         = Column(String(64), unique=True, nullable=False)
    llm_provider = Column(String(24), default="openai")
    llm_model    = Column(String(48), default="gpt-4o-mini")
    llm_api_key  = Column(LargeBinary)          # encrypted later

# 3️⃣  Auto-create DB & default row
Base.metadata.create_all(engine)

def get_workspace(name: str = "default") -> Workspace:
    """Return the workspace row (creates it if missing)."""
    session = SessionLocal()
    ws = session.query(Workspace).filter_by(name=name).first()
    if not ws:
        ws = Workspace(name=name)
        session.add(ws)
        session.commit()
    return ws
