from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from db.base import Base 


class Group(Base):

    __tablename__ = 'groups'
    
    id = Column(Integer(), primary_key=True)
    uuid = Column(Text())
    title = Column(Text())
    secretCode = Column(Text())

    user = relationship('users')
    day = relationship('days')
