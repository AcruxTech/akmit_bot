from sqlalchemy import create_engine, Integer, BigInteger, Float, Column
from db.main import get_base

class Person(get_base()):
  __tablename__ = 'Invites'
  id = Column('id', BigInteger(), primary_key=True)
  member_id = Column('member_id', BigInteger(), nullable=False)
  amount_msg = Column('amount_msg', Integer(),  nullable=False)
  available_amount_msg = Column('available_amount_msg', Float(), nullable=False)
  is_warned = Column('is_warned', Integer(), nullable=False)