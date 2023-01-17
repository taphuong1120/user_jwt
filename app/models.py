from app.database import Base
from sqlalchemy import Column, String, Boolean, text, Integer, DateTime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,unique =True)
    email = Column(String, unique=True)
    twitter = Column(String, unique=True,nullable=True)
    telegram = Column(String, unique=True,nullable=True)
    bio = Column(String, nullable=True)
    wallet = Column(String, nullable=True,unique =True)
    dnft = Column(Integer,default=0,nullable=True)
    dp = Column(Integer,default=0,nullable=True)
    password = Column(String)
    photo = Column(String, nullable=True)
    role = Column(Integer, default = 0, nullable = True)
    disabled = Column(Boolean, default=False)
   
    created_at = Column(DateTime(timezone=True), server_default=func.now(),nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(),nullable=True)
