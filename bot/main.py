import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from databases import Database
from sqlalchemy import MetaData, create_engine

from os import path, environ, listdir
from json import dumps, loads

from objects import globals
import asyncio

from loguru import logger
import psycopg2

async def main():
    if not path.exists("config.json"):
        with open(r"config.json", "w") as write_config:
            write_config.write(dumps({
                "token":None,
                "admin_username":None,
                "admin_chat_id":None,
                "qiwi_phone":None,
                "qiwi_token":None,
                "percent":0}))
            write_config.close()

    #with open(r"config.json", "r", encoding="utf-8") as load_config:
    #    globals.config = loads(load_config.read())
    globals.config = {
        "qiwi_token": eval(environ.get("QIWI_SECRET_KEY")),
        "qiwi_phone": eval(environ.get("QIWI_PHONE"))
    }

    logger.add(r"debug/debug.log", format="{time} {level} {message}",
        level="DEBUG", rotation="1 week", encoding="utf-8",
        compression="zip")

    #Database
    config = {
        "host": environ.get("POSTGRES_HOST"),
        "username": environ.get("POSTGRES_USERNAME"),
        "password": environ.get("POSTGRES_PASSWORD"),
        "port": environ.get("POSTGRES_PORT"),
        "name": environ.get("POSTGRES_NAME")
    }

    globals.db = Database("sqlite:///../web/db.sqlite3") # Database("postgres://%(username)s:%(password)s@%(host)s:%(port)s/%(name)s" % (config))
    globals.metadata = MetaData()
    globals.db_engine = create_engine(str(globals.db.url))
    globals.metadata.create_all(globals.db_engine)

    try:
        globals.bot = Bot(token=eval(environ.get("BOT_TOKEN")), parse_mode="html")
        logger.info("TG Bot loaded")
    except Exception as e: logger.error(e)
    globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

    import commands

    try:
        await globals.dp.start_polling()
    except Exception as e: logger.error(e)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:exit(0)