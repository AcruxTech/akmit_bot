from sqlalchemy import Column, ForeignKey, Integer, Text
from db.base import Base


class Lesson(Base):

    __tablename__ = 'lessons'
    
    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    pavilion = Column(Text())
    dayId = Column(Integer(), ForeignKey('days.id'))