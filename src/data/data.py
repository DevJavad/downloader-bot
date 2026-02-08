from typing import Literal
import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
MESSAGES_FILE = BASE_DIR / "messages.json"
ERRORS_FILE = BASE_DIR / "errors.json"

with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
    messages: dict[str, dict[str, str]] = json.load(f)

with open(ERRORS_FILE, "r", encoding="utf-8") as f:
    errors: dict[str, dict[str, str]] = json.load(f)


def get_user_message(
    key: str,
    language: Literal["en", "fa"] = "en",
    **kwargs
) -> str:
    message = messages.get(key, {}).get(language)
    return message.format(**kwargs)


def get_error_message(
    key: str,
    language: Literal["en", "fa"] = "en",
    **kwargs
) -> str:
    message = errors.get(key, {}).get(language)
    return message.format(**kwargs)