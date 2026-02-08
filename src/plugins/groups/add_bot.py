from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatJoinType
from database.models import Groups
from data import get_user_message
import logging


logger = logging.getLogger(__name__)


@Client.on_message(filters.new_chat_members & filters.group)
async def added_group(client: Client, message: Message):
    if message.chat_join_type == ChatJoinType.BY_ADD:
        me = await client.get_me()

        for member in message.new_chat_members:
            if member.is_bot and member.id == me.id:
                chat = message.chat.id
                group, status = await Groups.get_or_create(group_id=str(chat))

                if status:
                    logger.info("create a new group: %s", chat)
                    
                language = message.from_user.language_code if message.from_user.language_code in ["en", "fa"] else "en"
                return await client.send_message(chat, get_user_message("added_group", language, name=message.chat.title))