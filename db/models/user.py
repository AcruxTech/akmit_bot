from sqlalchemy import Column, ForeignKey, Integer, BigInteger, Text
from db.base import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger(), primary_key=True)
    name = Column(Text())
    classId = Column(Integer(), ForeignKey('groups.id'))