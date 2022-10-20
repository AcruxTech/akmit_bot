from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from main import config

db = config.db

Base = declarative_base()

def get_base():
    return Base

engine = create_engine(f'postgresql+psycopg2://{db.user}:{db.password}@{db.addr}/{db.name}')
engine.connect()



def init_db():
    Base.metadata.create_all(engine)
    print('Database is initialized')

def drop_table():
    Base.metadata.drop_all(engine)
    print('Database is droped')

if __name__ == 'main':
    init_db()