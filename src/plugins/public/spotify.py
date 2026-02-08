from pyrogram import Client, filters
from pyrogram.types import Message
from database.models import Users
from api.spotify import request
from data import get_user_message, get_error_message
import logging


logger = logging.getLogger(__name__)


@Client.on_message(filters.regex(r"https?:\/\/open\.spotify\.com\/track\/([A-Za-z0-9]+)"))
async def spotify(client: Client, message: Message):
    user_id = message.from_user.id
    user = await Users.get_or_none(user_id=str(user_id))
    language = user.language if user else None or message.from_user.language_code if message.from_user.language_code in ["en", "fa"] else "en"

    waiting = await message.reply(get_user_message("waiting", language))
    response = await request(client.request, message.text)
    url, info = response.get("url"), response.get("info")

    if not url:
        return await waiting.edit(get_error_message("no_response", language))

    await waiting.delete()
    return await message.reply_audio(
        url,
        caption=get_user_message(
            "spotify_caption",
            language,
            title=info.get("title"),
            cover=info.get("cover"),
            artist=info.get("artist"),
            album=info.get("album"),
            duration=info.get("duration")
        )
    )