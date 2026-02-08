from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo
from database.models import Users
from api.instagram import request
from data import get_user_message, get_error_message
from config import Config
import logging


logger = logging.getLogger(__name__)


@Client.on_message(
    filters.regex(
        r"(?i)\bhttps?:\/\/(?:www\.)?instagram\.com\/(?:p(?:ost)?|reel|tv|stories|story)?\/?[A-Za-z0-9._-]+(?:\/[A-Za-z0-9._-]*)*(?:\?[^\s#]*)?(?:#[^\s]*)?\b"
    )
)
async def instagram(client: Client, message: Message):
    user_id = message.from_user.id
    user = await Users.get_or_none(user_id=str(user_id))
    language = user.language if user else None or message.from_user.language_code if message.from_user.language_code in ["en", "fa"] else "en"

    waiting = await message.reply(get_user_message("waiting", language))
    response = await request(client.request, message.text)

    if not response:
        return await waiting.edit(get_error_message("no_response", language))

    videos = response.get("videos", [])
    images = response.get("images", [])

    await waiting.delete()
    if len(videos) == 1 and not images:
        return await message.reply_video(videos[0], caption=get_user_message("caption", language, bot_id=Config.BOT_ID))

    if len(videos) > 1 and not images:
        medias = [InputMediaVideo(video) for video in videos]
        return await message.reply_media_group(medias)

    if len(images) == 1 and not videos:
        return await message.reply_photo(images[0], caption=get_user_message("caption", language, bot_id=Config.BOT_ID))

    if len(images) > 1 and not videos:
        medias = [InputMediaPhoto(image) for image in images]
        return await message.reply_media_group(medias)

    if videos or images:
        medias = []

        for video in videos:
            medias.append(InputMediaVideo(video))

        for image in images:
            medias.append(InputMediaPhoto(image))

        return await message.reply_media_group(medias)