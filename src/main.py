from pyrogram import Client
from database import connect, disconnect
from api import Request
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S" 
)

file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

request = Request(50)
client = Client(
    "session",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="session",
    plugins=dict(root="plugins")
)


@client.on_start()
async def start(client):
    logger.info("Bot started")
    await request.connect()
    await connect(Config.DATABASE)
    client.request = request


@client.on_stop()
async def stop(client):
    logger.info("Bot stopped")
    await request.disconnect()
    await disconnect()


if __name__ == "__main__":
    client.run()