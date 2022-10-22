from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from db.base import Base
import db.models.user, db.models.group, db.models.day, db.models.lesson


class Worker():

    def __init__(self, config: dict):
        self.db = config
        self.engine = create_engine(
            f'postgresql+psycopg2://{self.db["user"]}:{self.db["password"]}@{self.db["addr"]}/{self.db["name"]}'
        )
        self.engine.connect()
        print('ok create engine')


    def create_all(self):
        Base.metadata.create_all(self.engine)
        print('Database is initialized')


    def drop_all(self):
        Base.metadata.drop_all(self.engine)
        print('Database is droped')