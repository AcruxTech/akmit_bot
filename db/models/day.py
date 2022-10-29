from sqlalchemy import Column, ForeignKey, BigInteger, Text

from db.base import Base


class Day(Base):

    __tablename__ = 'days'
    
    id = Column(BigInteger(), primary_key=True)
    name = Column(Text())
    pavilion = Column(Text())
    group_id = Column(BigInteger(), ForeignKey('groups.id'))
