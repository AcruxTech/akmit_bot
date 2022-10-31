from sqlalchemy import Column, BigInteger, Text
from db.base import Base 


class Group(Base):

    __tablename__ = 'groups'
    
    id = Column(BigInteger(), primary_key=True)
    uuid = Column(Text())
    title = Column(Text())
