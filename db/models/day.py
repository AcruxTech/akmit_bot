from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from db.base import Base


class Day(Base):

    __tablename__ = 'days'
    
    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    pavilion = Column(Text())
    lesson = relationship('lessons')

    classId = Column(Integer(), ForeignKey('groups.id'))