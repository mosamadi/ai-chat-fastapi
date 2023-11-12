import enum
from sqlalchemy import Column, Integer,String,ForeignKey,Enum,DateTime
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime


class IntractionRoleEnum(str,enum.Enum):
    SYSTEM = "System"
    HUMAN =  "Human"
    AI = "AI"

class Intraction(Base):
    __tablename__ = "intractions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"))
    name = Column(String)
    user  = relationship('UserModel', back_populates="interactions")
    messages =relationship('InteractionMessage', back_populates="intraction")

class InteractionMessage(Base):
    __tablename__ = "intercation_messages"
    id = Column(Integer, primary_key=True, index=True)
    intraction_id = Column(ForeignKey('intractions.id'))
    intraction  = relationship('Intraction', back_populates="messages")
    content = Column(String)
    role = Column(Enum(IntractionRoleEnum))
    created_at  = Column(DateTime,default=datetime.utcnow)