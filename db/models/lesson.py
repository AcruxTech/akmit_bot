from sqlalchemy import Column, ForeignKey, BigInteger, Text

from db.base import Base
from db.models.model import Model


class Lesson(Base, Model):

    __tablename__ = 'lessons'
    
    name = Column(Text())
    pavilion = Column(Text())
    dayId = Column(BigInteger, ForeignKey('days.id'))