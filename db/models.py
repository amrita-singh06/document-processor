from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from config import SQLITE_DB_PATH

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String)

engine = create_engine(f"sqlite:///{SQLITE_DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
