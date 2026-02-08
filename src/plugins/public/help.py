from pyrogram import Client, filters
from pyrogram.types import Message
from database.models import Users
from data import get_user_message
import logging


logger = logging.getLogger(__name__)


@Client.on_message(filters.command("help"))
async def start(client: Client, message: Message):
    user = await Users.get_or_none(user_id=str(message.from_user.id))
    language = user.language if user else None or message.from_user.language_code if message.from_user.language_code in ["en", "fa"] else "en"
    await message.reply(get_user_message("help", language))