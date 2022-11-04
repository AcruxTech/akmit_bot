from sqlalchemy import Column, ForeignKey, BigInteger, Text

from db.base import Base


class Lesson(Base):

    __tablename__ = 'lessons'
    
    id = Column(BigInteger(), primary_key=True)
    title = Column(Text())
    homework = Column(Text())
    date = Column(Text())                       # dd.mm.yy
    group_id = Column(BigInteger(), ForeignKey('groups.id'))
