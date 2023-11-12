from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    full_name = Column(String)
    interactions =  relationship('Intraction', back_populates="user")