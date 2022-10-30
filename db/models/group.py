from uuid import uuid4

from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import relationship
from db.base import Base 


class Group(Base):

    __tablename__ = 'groups'
    
    id = Column(BigInteger(), primary_key=True)
    uuid = Column(Text())
    title = Column(Text())
    secretCode = Column(Text())


default_group = Group(id = 1, uuid = uuid4(), title = 'default', secretCode = 100)
