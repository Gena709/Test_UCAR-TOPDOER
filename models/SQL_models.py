from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
import datetime
from contextlib import contextmanager

engine = create_engine('sqlite:///topdoer_database.db')

Base = declarative_base()


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    incidents = relationship("Incident", backref="status")


class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    description = Column(Text, nullable=True)
    status_id = Column(Integer, ForeignKey("status.id"))
    source = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


session = sessionmaker(engine)
Base.metadata.create_all(engine)


@contextmanager
def session_manager() -> Session:
    db = session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
