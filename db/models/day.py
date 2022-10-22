from sqlalchemy import Column, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship

from db.base import Base
from db.models.model import Model


class Day(Base, Model):

    __tablename__ = 'days'
    
    name = Column(Text())
    pavilion = Column(Text())
    lesson = relationship('lessons')

    classId = Column(BigInteger(), ForeignKey('groups.id'))