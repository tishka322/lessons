from app.backend.db import Base
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import User



class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    slug = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    user = relationship('User', back_populates='tasks')

from sqlalchemy.schema import CreateTable

print(CreateTable(Task.__table__))

