from sqlalchemy import Column, ForeignKey, BigInteger, Text, Integer
from sqlalchemy.orm import relationship

from db.base import Base
from db.models.model import Model


class Lesson(Base, Model):

    __tablename__ = 'lessons'
    
    name = Column(Text())
    pavilion = Column(Text())
    day = Column(BigInteger, ForeignKey('days.id'))
