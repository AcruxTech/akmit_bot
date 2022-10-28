from uuid import uuid4

from sqlalchemy import Integer, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base 
from db.models.model import Model


class Group(Base, Model):

    __tablename__ = 'groups'
    
    uuid = Column(Text())
    title = Column(Text())
    secretCode = Column(Text())


default_group = Group(uuid = uuid4(), title = 'default', secretCode = 100)