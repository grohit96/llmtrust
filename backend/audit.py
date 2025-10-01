# backend/audit.py
import os
import json
import datetime
from sqlalchemy import create_engine, Column, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# DB file in project root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audit_log.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

Base = declarative_base()

class AuditEntry(Base):
    __tablename__ = "audit_log"
    id = Column(String, primary_key=True)      # audit_id
    response_id = Column(String)
    query = Column(Text)
    answer = Column(Text)
    citations = Column(Text)                   # stored as JSON
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def log_audit(response: dict):
    """Log a response to the audit trail."""
    session = Session()
    entry = AuditEntry(
        id=response["audit_id"],
        response_id=response["response_id"],
        query=response.get("query", ""),
        answer=response["answer"],
        citations=json.dumps(response["citations"]),
        confidence=response["confidence"],
    )
    session.add(entry)
    session.commit()
    session.close()

def get_audit_by_id(audit_id: str):
    """Retrieve a logged response by audit_id."""
    session = Session()
    entry = session.get(AuditEntry, audit_id)
    if not entry:
        session.close()
        return {"error": "Audit entry not found"}

    data = {
        "audit_id": entry.id,
        "response_id": entry.response_id,
        "query": entry.query,
        "answer": entry.answer,
        "citations": json.loads(entry.citations),
        "confidence": entry.confidence,
        "timestamp": entry.timestamp.isoformat(),
    }
    session.close()
    return data
