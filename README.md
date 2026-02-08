# downloader-bot
A Telegram bot to download content from instagram and spotify.


## Start
```bash
git clone https://github.com/DevJavad/downloader-bot.git
cd src
pip install requirements.txt
python main.py
```

## ⚙️ Configuration

Before running the project, open the config file and enter your credentials.

- Path:
`src/config/config.py`

Edit this file and fill in the required values:

```python
class Config:
    API_ID: int = ...
    BOT_ID: str = ""
    DATABASE: str = "sqlite://./database.sqlite"
    API_HASH: str = ""
    BOT_TOKEN: str = ""
```

Required fields:
- API_ID – Telegram API ID
- API_HASH – Telegram API Hash
- BOT_TOKEN – Bot token from @BotFather
- BOT_ID – Your bot ID
- DATABASE – Database URL (default uses SQLite)

After filling in the values, save the file and run the project.