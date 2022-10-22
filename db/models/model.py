from sqlalchemy import Column, BigInteger


class Model():
    
    __abstract__ = True
    
    id = Column(BigInteger(), primary_key=True)