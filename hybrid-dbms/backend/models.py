from sqlalchemy import Column, Text, JSON, TIMESTAMP, String
from sqlalchemy.sql import func
from db import Base

class Record(Base):
    __tablename__ = "records"
    id = Column(String(36), primary_key=True)
    title = Column(Text)
    structured_json = Column(JSON)
    mongo_doc_id = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
