from sqlalchemy import Integer, Column, String, TIMESTAMP, func, Text
from .db import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    title = Column(String)
    description = Column(Text)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=func.now())