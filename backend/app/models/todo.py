from datetime import datetime
from app.db.base_class import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
