from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship

from db.base import Base 
from db.models.model import Model

class Group(Base, Model):

    __tablename__ = 'groups'
    
    uuid = Column(Text())
    title = Column(Text())
    secretCode = Column(Text())

    user = relationship('users')
    day = relationship('days')
