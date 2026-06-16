## DATABASE SCHEMA

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    doc_id = Column(String, unique=True)
    filename = Column(String)
    file_type = Column(String)
    author = Column(String, nullable=True)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    page_count = Column(Integer)
    status = Column(String, default="processed")
    
engine = create_engine("sqlite:///documents.db")
Base.metadata.create_all(engine)
Sessionlocal = sessionmaker(bind=engine)