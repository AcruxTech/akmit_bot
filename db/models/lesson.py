from sqlalchemy import Column, ForeignKey, BigInteger, Text

from db.base import Base


class Lesson(Base):

    __tablename__ = 'lessons'
    
    id = Column(BigInteger(), primary_key=True)
    name = Column(Text())
    pavilion = Column(Text())
    day = Column(BigInteger, ForeignKey('days.id'))
