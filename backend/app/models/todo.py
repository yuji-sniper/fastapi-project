from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.db.base_class import Base


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(64))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    user = relationship("User", back_populates="todos")
