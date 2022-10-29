from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine

from db.base import Base
import db.models.user, db.models.group, db.models.day, db.models.lesson


class Worker():

    def __init__(self, config: dict, logger: Logger = None):
        self._db = config
        self._engine = create_engine(
            f'''postgresql+psycopg2://{self._db["user"]}:{self._db["password"]}@{self._db["addr"]}/{self._db["name"]}'''
        )
        self._engine.connect()
        self._logger = logger
        print(f'Create engine for {self._db["name"]}')
        self._logger.info(f'Create engine for {self._db["name"]}')

    
    def get_engine(self) -> Engine:
        return self._engine


    def create_all(self):
        Base.metadata.create_all(self._engine)
        self._logger.info(f'All tables of {self._db["name"]} created')


    def drop_all(self):
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self._logger.info(f'All tables of {self._db["name"]} dropped')
