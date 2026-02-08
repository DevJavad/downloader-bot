from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from database.models import Users
from data import get_user_message
import logging


logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    user = None
    language = message.from_user.language_code if message.from_user.language_code in ["en", "fa"] else "en"

    if message.chat.type == ChatType.PRIVATE:
        user, status = await Users.get_or_create(
            user_id=str(message.from_user.id),
            defaults={"language": language}
        )

        if status:
            logger.info("create a new user: %s", user.user_id)

        if user.language:
            language = user.language

    await message.reply(get_user_message("start", language, name=message.from_user.full_name))