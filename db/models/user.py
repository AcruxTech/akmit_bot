from sqlalchemy import Column, ForeignKey, Integer, BigInteger, Text

from db.base import Base


class User(Base):
    
    __tablename__ = 'users'
    
    id = Column(BigInteger(), primary_key=True)
    uuid = Column(BigInteger())             # telegram unique id: int
    name = Column(Text())
    group_id = Column(Integer(), ForeignKey('groups.id'), nullable=True)

    
    def __repr__(self):
        return f'User({self.id}, {self.uuid}, {self.name}, {self.group_id})'
