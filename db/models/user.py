from sqlalchemy import Column, ForeignKey, Integer, BigInteger, Text

from db.base import Base
from db.models.model import Model


class User(Base, Model):
    
    __tablename__ = 'users'
    
    name = Column(Text())
    group_id = Column(Integer(), ForeignKey('groups.id'))