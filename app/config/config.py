import os
import dotenv

from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Db:
    user: str
    password: str
    addr: str
    name: str


@dataclass
class Config:
    tg_bot: TgBot
    db: Db


def load_config():
    dotenv.load_dotenv()

    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN')
        ),
        db=Db(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            addr=os.getenv('DB_ADDR'),
            name=os.getenv('DB_NAME')
        )
    )