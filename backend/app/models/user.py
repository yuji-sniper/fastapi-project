from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(32))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
