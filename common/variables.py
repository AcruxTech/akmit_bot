import logging

from db.worker import Worker
from app.config.config import load_config 


logger = logging.getLogger(__name__)
config = load_config()
worker = Worker(config.db.__dict__, logger)
engine = worker.get_engine()
